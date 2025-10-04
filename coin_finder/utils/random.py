from __future__ import annotations

import os
from hashlib import sha3_256
from typing import Iterable


class HashStreamRNG:
    """
    Deterministic cryptographic PRNG based on SHA3-256 in counter mode.

    This generator is not meant to replace `secrets` for long-term key storage,
    but it is suitable for high-throughput generation of candidate private keys
    when fed with strong seed material. Seed material should include both a
    user-provided value (``--seed``) and a high-resolution timestamp so that
    parallel workers diverge safely.
    """

    def __init__(self, seed_material: bytes) -> None:
        if not seed_material:
            raise ValueError("seed_material must not be empty")
        self._root = sha3_256(seed_material).digest()
        self._counter = 0

    def _next_block(self) -> bytes:
        counter_bytes = self._counter.to_bytes(16, "big")
        self._counter += 1
        return sha3_256(self._root + counter_bytes).digest()

    def get_bytes(self, n: int) -> bytes:
        if n <= 0:
            raise ValueError("n must be positive")
        chunks = bytearray()
        while len(chunks) < n:
            chunks.extend(self._next_block())
        return bytes(chunks[:n])

    def get_uint(self, bit_size: int) -> int:
        if bit_size <= 0:
            raise ValueError("bit_size must be positive")
        byte_len = (bit_size + 7) // 8
        value = int.from_bytes(self.get_bytes(byte_len), "big")
        mask = (1 << bit_size) - 1
        return value & mask

    @classmethod
    def from_seed_components(
        cls,
        seed: str | bytes | None,
        *components: Iterable[int] | bytes | str | None,
        include_os_entropy: bool = True,
    ) -> "HashStreamRNG":
        """
        Build a generator by hashing together arbitrary seed components.

        Parameters
        ----------
        seed:
            Base seed supplied by the user (``--seed``). May be ``None``.
        components:
            Additional entropy sources, e.g. timestamps, worker IDs, counters.
        include_os_entropy:
            When True, mixes in 16 bytes from ``os.urandom`` to ensure that two
            invocations with identical parameters diverge.
        """
        material = bytearray()

        def _extend(value: bytes | str | Iterable[int] | None) -> None:
            if value is None:
                return
            if isinstance(value, bytes):
                material.extend(value)
            elif isinstance(value, str):
                material.extend(value.encode("utf-8"))
            else:
                for item in value:
                    material.extend(int(item).to_bytes(8, "big", signed=False))

        _extend(seed)
        for component in components:
            _extend(component)
        if include_os_entropy:
            material.extend(os.urandom(16))
        return cls(bytes(material))
