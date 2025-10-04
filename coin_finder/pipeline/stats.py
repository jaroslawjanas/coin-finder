from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class StatsSnapshot:
    timestamp: float
    uptime: float
    total_batches: int
    total_keys_generated: int
    total_requests: int
    total_hits: int
    total_errors: int
    last_batch_duration_ms: float
    last_rpc_latency_ms: float
    last_hit: Optional[str]
    requests_per_sec: float
    keys_per_sec: float
    hits_per_sec: float


@dataclass
class _MutableStats:
    start_time: float = field(default_factory=time.perf_counter)
    total_batches: int = 0
    total_keys_generated: int = 0
    total_requests: int = 0
    total_hits: int = 0
    total_errors: int = 0
    last_batch_duration_ms: float = 0.0
    last_rpc_latency_ms: float = 0.0
    last_hit: Optional[str] = None
    history: list[tuple[float, int, int, int]] = field(default_factory=list)  # (timestamp, requests, keys, hits)

    def add_history_point(self) -> None:
        now = time.perf_counter()
        self.history.append((now, self.total_requests, self.total_keys_generated, self.total_hits))
        # Keep only the last few seconds of history for rate calculation
        cutoff = now - 10.0
        while self.history and self.history[0][0] < cutoff:
            self.history.pop(0)

    def to_snapshot(self) -> StatsSnapshot:
        now = time.perf_counter()
        uptime = now - self.start_time
        requests_per_sec = keys_per_sec = hits_per_sec = 0.0
        if len(self.history) >= 2:
            t0, req0, key0, hit0 = self.history[0]
            t1, req1, key1, hit1 = self.history[-1]
            dt = max(t1 - t0, 1e-6)
            requests_per_sec = (req1 - req0) / dt
            keys_per_sec = (key1 - key0) / dt
            hits_per_sec = (hit1 - hit0) / dt
        return StatsSnapshot(
            timestamp=time.time(),
            uptime=uptime,
            total_batches=self.total_batches,
            total_keys_generated=self.total_keys_generated,
            total_requests=self.total_requests,
            total_hits=self.total_hits,
            total_errors=self.total_errors,
            last_batch_duration_ms=self.last_batch_duration_ms,
            last_rpc_latency_ms=self.last_rpc_latency_ms,
            last_hit=self.last_hit,
            requests_per_sec=requests_per_sec,
            keys_per_sec=keys_per_sec,
            hits_per_sec=hits_per_sec,
        )


class Statistics:
    def __init__(self) -> None:
        self._stats = _MutableStats()
        self._lock = asyncio.Lock()
        self._stats.add_history_point()

    async def record_batch(
        self,
        *,
        keys_generated: int,
        requests_made: int,
        hits: int,
        errors: int,
        batch_duration_ms: float,
        rpc_latency_ms: float,
        last_hit: Optional[str],
    ) -> None:
        async with self._lock:
            self._stats.total_batches += 1
            self._stats.total_keys_generated += keys_generated
            self._stats.total_requests += requests_made
            self._stats.total_hits += hits
            self._stats.total_errors += errors
            self._stats.last_batch_duration_ms = batch_duration_ms
            self._stats.last_rpc_latency_ms = rpc_latency_ms
            if last_hit is not None:
                self._stats.last_hit = last_hit
            self._stats.add_history_point()

    async def record_error(self, count: int = 1) -> None:
        async with self._lock:
            self._stats.total_errors += count
            self._stats.add_history_point()

    async def snapshot(self) -> StatsSnapshot:
        async with self._lock:
            return self._stats.to_snapshot()
