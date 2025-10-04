from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

TOTAL_PRIVATE_KEYS = 1 << 160
FUNDED_ADDRESSES_ESTIMATE = 110_000_000  # Approximate funded Ethereum addresses (Oct 2025)
HIT_CHANCE_DENOMINATOR = TOTAL_PRIVATE_KEYS / FUNDED_ADDRESSES_ESTIMATE


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
    lifetime_runtime: float
    lifetime_total_keys: int
    lifetime_total_hits: int
    lifetime_keys_per_sec: float
    lifetime_hit_chance: float


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
        cutoff = now - 10.0
        while self.history and self.history[0][0] < cutoff:
            self.history.pop(0)

    def to_snapshot(
        self,
        *,
        lifetime_runtime: float,
        lifetime_total_keys: int,
        lifetime_total_hits: int,
        lifetime_keys_per_sec: float,
        lifetime_hit_chance: float,
    ) -> StatsSnapshot:
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
            lifetime_runtime=lifetime_runtime,
            lifetime_total_keys=lifetime_total_keys,
            lifetime_total_hits=lifetime_total_hits,
            lifetime_keys_per_sec=lifetime_keys_per_sec,
            lifetime_hit_chance=lifetime_hit_chance,
        )


@dataclass
class LifetimeStats:
    total_runtime_seconds: float = 0.0
    total_keys_generated: int = 0
    total_hits: int = 0

    def to_dict(self) -> dict[str, float | int]:
        return {
            "total_runtime_seconds": self.total_runtime_seconds,
            "total_keys_generated": self.total_keys_generated,
            "total_hits": self.total_hits,
        }

    @classmethod
    def from_path(cls, path: Path) -> LifetimeStats:
        if path is None or not path.exists():
            return cls()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return cls()
        return cls(
            total_runtime_seconds=float(raw.get("total_runtime_seconds", 0.0)),
            total_keys_generated=int(raw.get("total_keys_generated", 0)),
            total_hits=int(raw.get("total_hits", 0)),
        )


class Statistics:
    def __init__(self, *, store_path: Path | None = None, save_interval: float = 5.0) -> None:
        self._stats = _MutableStats()
        self._lock = asyncio.Lock()
        self._store_path = store_path
        self._save_interval = max(save_interval, 1.0)
        session_start = time.perf_counter()
        self._session_start = session_start
        self._last_persist = session_start

        if self._store_path is not None:
            self._store_path.parent.mkdir(parents=True, exist_ok=True)
            self._lifetime = LifetimeStats.from_path(self._store_path)
            self._base_runtime = self._lifetime.total_runtime_seconds
        else:
            self._lifetime = LifetimeStats()
            self._base_runtime = 0.0

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

            self._lifetime.total_keys_generated += keys_generated
            self._lifetime.total_hits += hits

            self._maybe_persist_locked()

    async def record_error(self, count: int = 1) -> None:
        async with self._lock:
            self._stats.total_errors += count
            self._stats.add_history_point()
            self._maybe_persist_locked()

    async def snapshot(self) -> StatsSnapshot:
        async with self._lock:
            now = time.perf_counter()
            lifetime_runtime = self._base_runtime + (now - self._session_start)
            lifetime_keys = self._lifetime.total_keys_generated
            lifetime_hits = self._lifetime.total_hits
            lifetime_keys_per_sec = lifetime_keys / lifetime_runtime if lifetime_runtime > 0 else 0.0
            lifetime_hit_chance = lifetime_keys / HIT_CHANCE_DENOMINATOR if lifetime_keys > 0 else 0.0
            snapshot = self._stats.to_snapshot(
                lifetime_runtime=lifetime_runtime,
                lifetime_total_keys=lifetime_keys,
                lifetime_total_hits=lifetime_hits,
                lifetime_keys_per_sec=lifetime_keys_per_sec,
                lifetime_hit_chance=lifetime_hit_chance,
            )
            self._maybe_persist_locked(now=now)
            return snapshot

    async def close(self) -> None:
        async with self._lock:
            self._maybe_persist_locked(force=True)

    def _maybe_persist_locked(self, *, now: float | None = None, force: bool = False) -> None:
        if self._store_path is None:
            return

        now = now or time.perf_counter()
        if not force and (now - self._last_persist) < self._save_interval:
            return

        total_runtime = self._base_runtime + (now - self._session_start)
        self._base_runtime = total_runtime
        self._session_start = now
        self._lifetime.total_runtime_seconds = total_runtime

        tmp_path = self._store_path.with_suffix(".tmp")
        try:
            with tmp_path.open("w", encoding="utf-8") as handle:
                json.dump(self._lifetime.to_dict(), handle, indent=2)
            tmp_path.replace(self._store_path)
        except OSError:
            # Ignore persistence errors; statistics are best-effort
            tmp_path.unlink(missing_ok=True)
        finally:
            self._last_persist = now
