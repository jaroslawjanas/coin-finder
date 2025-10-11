from __future__ import annotations

import asyncio
import logging
from contextlib import suppress
from typing import Iterable, Sequence

from coin_finder.chains.eth.rpc import EthBalanceClient
from coin_finder.config import AppConfig
from coin_finder.logging_config import configure_logging
from coin_finder.pipeline.csv_writer import AsyncCSVWriter
from coin_finder.pipeline.stats import Statistics
from coin_finder.pipeline.worker import run_worker
from coin_finder.rpc.http_client import JsonRpcHttpClient
from coin_finder.ui.dashboard import dashboard_loop

logger = logging.getLogger(__name__)

CSV_HEADERS: Sequence[str] = (
    "public_key_hex",
    "address",
    "balance_wei",
    "balance_eth",
    "detected_at",
)


async def _async_main(config: AppConfig) -> None:
    stats = Statistics(store_path=config.output_dir / "stats.json")
    stop_event = asyncio.Event()
    csv_writer = AsyncCSVWriter(config.hits_path, headers=CSV_HEADERS)

    async with JsonRpcHttpClient(
        config.eth_rpc_url,
        max_outstanding_requests=config.rpc_max_outstanding_requests,
        timeout=config.rpc_timeout,
    ) as rpc_client:
        balance_client = EthBalanceClient(rpc_client)
        worker_tasks = [
            asyncio.create_task(
                run_worker(
                    worker_id=i,
                    config=config,
                    balance_client=balance_client,
                    csv_writer=csv_writer,
                    stats=stats,
                    stop_event=stop_event,
                ),
                name=f"worker-{i}",
            )
            for i in range(config.workers)
        ]
        dashboard_task = asyncio.create_task(
            dashboard_loop(
                stats,
                stop_event,
                refresh_interval=config.stats_refresh_interval,
            ),
            name="dashboard",
        )

        try:
            await asyncio.Event().wait()
        finally:
            stop_event.set()
            logger.info("Shutting down workers...")
            for task in worker_tasks:
                task.cancel()
            dashboard_task.cancel()
            with suppress(asyncio.CancelledError):
                await asyncio.gather(*worker_tasks, return_exceptions=True)
                await asyncio.gather(dashboard_task, return_exceptions=True)
            await stats.close()


def run(config: AppConfig) -> None:
    configure_logging(config.log_level)
    logger.info(
        "Starting coin-finder with %s workers, batch size %s",
        config.workers,
        config.batch_size,
    )
    try:
        asyncio.run(_async_main(config))
    except KeyboardInterrupt:
        logger.info("Interrupted by user, stopping...")
    except Exception:
        logger.exception("coin-finder terminated due to an unexpected error")
        raise
