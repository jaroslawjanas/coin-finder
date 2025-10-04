from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence

import aiohttp
import backoff
from aiohttp import ClientConnectorError, ClientResponseError, ClientSession, ServerTimeoutError
from anyio import CapacityLimiter

logger = logging.getLogger(__name__)

JsonDict = Dict[str, Any]


@dataclass(slots=True)
class JsonRpcRequest:
    method: str
    params: Sequence[Any]
    request_id: int


@dataclass(slots=True)
class JsonRpcResponse:
    request_id: int
    result: Any | None
    error: JsonDict | None


class JsonRpcBatchError(Exception):
    pass


def _is_retryable_error(exc: Exception) -> bool:
    if isinstance(exc, ClientResponseError):
        return exc.status >= 500 or exc.status in (408, 409, 425, 429, 499)
    if isinstance(exc, (ClientConnectorError, ServerTimeoutError)):
        return True
    return False


def _backoff_hdlr(details: Dict[str, Any]) -> None:
    wait = details["wait"]
    tries = details["tries"]
    value = details.get("value")
    logger.warning(
        "JsonRPC retry #%s in %.2fs, last response=%s",
        tries,
        wait,
        value,
    )


class JsonRpcHttpClient:
    def __init__(
        self,
        endpoint: str,
        *,
        session: ClientSession | None = None,
        headers: Dict[str, str] | None = None,
        max_outstanding_requests: int = 20,
        timeout: float = 30.0,
        json_rpc_version: str = "2.0",
    ) -> None:
        self._endpoint = endpoint
        self._headers = headers or {}
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session = session
        self._owns_session = session is None
        self._json_rpc_version = json_rpc_version
        self._limiter = CapacityLimiter(max_outstanding_requests)
        self._request_counter = 0
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> "JsonRpcHttpClient":
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None

    async def close(self) -> None:
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None

    def _build_payload(self, requests: Iterable[JsonRpcRequest]) -> List[JsonDict]:
        payload: List[JsonDict] = []
        for req in requests:
            payload.append(
                {
                    "jsonrpc": self._json_rpc_version,
                    "method": req.method,
                    "params": list(req.params),
                    "id": req.request_id,
                }
            )
        return payload

    async def batch_call(self, requests: Sequence[JsonRpcRequest]) -> tuple[List[JsonRpcResponse], float]:
        if not requests:
            return [], 0.0
        async with self._limiter:
            response_payload, latency_ms = await self._send_with_retry(self._build_payload(requests))
        response_index = {item["id"]: item for item in response_payload}
        responses: List[JsonRpcResponse] = []
        for req in requests:
            entry = response_index.get(req.request_id)
            if entry is None:
                raise JsonRpcBatchError(f"missing response for id {req.request_id}")
            responses.append(
                JsonRpcResponse(
                    request_id=req.request_id,
                    result=entry.get("result"),
                    error=entry.get("error"),
                )
            )
        return responses, latency_ms

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=5,
        giveup=lambda exc: not _is_retryable_error(exc),
        max_time=60,
        jitter=backoff.random_jitter,
        on_backoff=_backoff_hdlr,
    )
    async def _send_with_retry(self, payload: List[JsonDict]) -> tuple[List[JsonDict], float]:
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        if not self._session:
            raise RuntimeError("Client session not initialized")

        request_start = time.perf_counter()
        async with self._session.post(
            self._endpoint,
            json=payload,
            headers=self._headers,
        ) as resp:
            resp.raise_for_status()
            body = await resp.json(content_type=None)
        elapsed = (time.perf_counter() - request_start) * 1000.0
        if not isinstance(body, list):
            raise JsonRpcBatchError(f"expected list response, got {type(body)}")
        logger.debug("JsonRPC batch size=%s latency=%.1fms", len(payload), elapsed)
        return body, elapsed

    async def next_request_id(self) -> int:
        async with self._lock:
            self._request_counter += 1
            return self._request_counter
