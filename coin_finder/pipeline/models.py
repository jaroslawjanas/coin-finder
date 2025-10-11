from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from typing import Optional

getcontext().prec = 40  # High precision for ETH balances


@dataclass(slots=True)
class KeyCandidate:
    address: str
    public_key: bytes
    worker_id: int
    batch_id: int
    index: int
    seed_descriptor: str
    generated_at: float

    @property
    def public_key_hex(self) -> str:
        return self.public_key.hex()


@dataclass(slots=True)
class HitRecord:
    address: str
    public_key_hex: str
    balance_wei: int
    balance_eth: str
    worker_id: int
    batch_id: int
    index: int
    provider: str
    seed_descriptor: str
    detected_at_iso: str

    @classmethod
    def from_candidate(
        cls,
        candidate: KeyCandidate,
        *,
        balance_wei: int,
        provider: str,
    ) -> "HitRecord":
        balance_eth = Decimal(balance_wei) / Decimal(10**18)
        return cls(
            address=candidate.address,
            public_key_hex=candidate.public_key_hex,
            balance_wei=balance_wei,
            balance_eth=f"{balance_eth:.18f}",
            worker_id=candidate.worker_id,
            batch_id=candidate.batch_id,
            index=candidate.index,
            provider=provider,
            seed_descriptor=candidate.seed_descriptor,
            detected_at_iso=datetime.now(timezone.utc).isoformat(),
        )
