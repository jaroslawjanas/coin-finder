from __future__ import annotations

import asyncio
import csv
from pathlib import Path
from typing import Iterable

from coin_finder.pipeline.models import HitRecord


class AsyncCSVWriter:
    def __init__(self, path: Path, *, headers: Iterable[str]) -> None:
        self._path = path
        self._headers = list(headers)
        self._lock = asyncio.Lock()
        self._initialized = False

    async def append_hits(self, hits: Iterable[HitRecord]) -> None:
        hits_list = list(hits)
        if not hits_list:
            return
        async with self._lock:
            await asyncio.to_thread(self._append_sync, hits_list)

    def _append_sync(self, hits: list[HitRecord]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        file_exists = self._path.exists()
        with self._path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self._headers)
            if not file_exists:
                writer.writeheader()
            for hit in hits:
                writer.writerow(
                    {
                        "detected_at": hit.detected_at_iso,
                        "address": hit.address,
                        "private_key_hex": hit.private_key_hex,
                        "public_key_hex": hit.public_key_hex,
                        "balance_wei": str(hit.balance_wei),
                        "balance_eth": hit.balance_eth,
                        "worker_id": hit.worker_id,
                        "batch_id": hit.batch_id,
                        "batch_index": hit.index,
                        "provider": hit.provider,
                        "seed_descriptor": hit.seed_descriptor,
                    }
                )
