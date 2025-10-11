from __future__ import annotations

import asyncio
import logging
import time

from coin_finder.chains.eth.keygen import generate_eth_public_key_material
from coin_finder.config import AppConfig
from coin_finder.pipeline.csv_writer import AsyncCSVWriter
from coin_finder.pipeline.models import HitRecord, KeyCandidate
from coin_finder.pipeline.stats import Statistics
from coin_finder.utils.random import HashStreamRNG
from coin_finder.chains.eth.rpc import BalanceResult, EthBalanceClient


logger = logging.getLogger(__name__)


async def run_worker(
    worker_id: int,
    *,
    config: AppConfig,
    balance_client: EthBalanceClient,
    csv_writer: AsyncCSVWriter,
    stats: Statistics,
    stop_event: asyncio.Event,
) -> None:
    batch_id = 0
    provider = config.provider_name
    base_seed = config.seed or ""
    while not stop_event.is_set():
        batch_start = time.perf_counter()
        timestamp_ns = time.time_ns()
        timestamp_bytes = timestamp_ns.to_bytes(16, "big", signed=False)
        rng = HashStreamRNG.from_seed_components(
            base_seed,
            str(worker_id),
            str(batch_id),
            timestamp_bytes,
        )
        candidates: list[KeyCandidate] = []
        for index in range(config.batch_size):
            if stop_event.is_set():
                break
            material = generate_eth_public_key_material(rng)
            candidates.append(
                KeyCandidate(
                    address=material.address,
                    public_key=material.public_key,
                    worker_id=worker_id,
                    batch_id=batch_id,
                    index=index,
                    seed_descriptor=f"{base_seed}:{worker_id}:{batch_id}:{timestamp_ns}",
                    generated_at=time.perf_counter(),
                )
            )

        if not candidates:
            break

        addresses = [candidate.address for candidate in candidates]
        hits: list[HitRecord] = []
        errors = 0
        rpc_latency_ms = 0.0
        try:
            balance_results, rpc_latency_ms = await balance_client.get_balances(addresses)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Worker %s batch %s balance lookup failed: %s", worker_id, batch_id, exc)
            await stats.record_error()
            await asyncio.sleep(1.0)
            continue

        balance_by_address: dict[str, BalanceResult] = {result.address: result for result in balance_results}
        if len(balance_results) != len(candidates):
            missing = len(candidates) - len(balance_results)
            if missing > 0:
                errors += missing
                logger.debug(
                    "Worker %s batch %s missing %s balance results",
                    worker_id,
                    batch_id,
                    missing,
                )

        for candidate in candidates:
            result = balance_by_address.get(candidate.address)
            if result is None:
                errors += 1
                continue
            if result.error:
                errors += 1
                continue
            if result.balance_wei > 0:
                hits.append(
                    HitRecord.from_candidate(
                        candidate,
                        balance_wei=result.balance_wei,
                        provider=provider,
                    )
                )

        if hits:
            await csv_writer.append_hits(hits)

        batch_duration_ms = (time.perf_counter() - batch_start) * 1000.0
        last_hit_desc = hits[-1].address if hits else None
        await stats.record_batch(
            keys_generated=len(candidates),
            requests_made=len(addresses),
            hits=len(hits),
            errors=errors,
            batch_duration_ms=batch_duration_ms,
            rpc_latency_ms=rpc_latency_ms,
            last_hit=last_hit_desc,
        )
        batch_id += 1
