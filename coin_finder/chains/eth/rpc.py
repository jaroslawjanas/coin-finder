from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from coin_finder.rpc.http_client import JsonRpcHttpClient, JsonRpcRequest, JsonRpcResponse


@dataclass(slots=True)
class BalanceResult:
    address: str
    balance_wei: int
    error: dict | None


class EthBalanceClient:
    def __init__(
        self,
        rpc_client: JsonRpcHttpClient,
        *,
        tag: str = "latest",
    ) -> None:
        self._client = rpc_client
        self._tag = tag

    async def get_balances(self, addresses: Sequence[str]) -> Tuple[List[BalanceResult], float]:
        if not addresses:
            return [], 0.0

        requests: List[JsonRpcRequest] = []
        for address in addresses:
            request_id = await self._client.next_request_id()
            requests.append(
                JsonRpcRequest(
                    method="eth_getBalance",
                    params=[address, self._tag],
                    request_id=request_id,
                )
            )

        responses, latency_ms = await self._client.batch_call(requests)
        response_by_id: dict[int, JsonRpcResponse] = {resp.request_id: resp for resp in responses}

        results: List[BalanceResult] = []
        for request in requests:
            response = response_by_id.get(request.request_id)
            if response is None:
                results.append(
                    BalanceResult(
                        address=request.params[0],
                        balance_wei=0,
                        error={"code": -32603, "message": "missing response"},
                    )
                )
                continue
            if response.error:
                results.append(
                    BalanceResult(
                        address=request.params[0],
                        balance_wei=0,
                        error=response.error,
                    )
                )
            else:
                result_hex = response.result or "0x0"
                results.append(
                    BalanceResult(
                        address=request.params[0],
                        balance_wei=int(result_hex, 16),
                        error=None,
                    )
                )
        return results, latency_ms
