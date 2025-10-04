from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from coincurve import PrivateKey
from eth_utils import keccak, to_checksum_address

from coin_finder.utils.random import HashStreamRNG

# Order of the secp256k1 curve used by Ethereum
_SECP256K1_N = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)


class SupportsGetBytes(Protocol):
    def get_bytes(self, n: int) -> bytes:
        ...


@dataclass(slots=True)
class EthKeyMaterial:
    private_key: bytes
    public_key: bytes
    address: str

    @property
    def private_key_hex(self) -> str:
        return self.private_key.hex()

    @property
    def public_key_hex(self) -> str:
        return self.public_key.hex()


def _generate_private_key_bytes(source: SupportsGetBytes) -> bytes:
    """
    Draw 32 random bytes and ensure the resulting integer is in the correct range.

    Ethereum private keys are 32-byte integers in the range [1, secp256k1.n - 1].
    We use rejection sampling to avoid bias.
    """
    while True:
        candidate = source.get_bytes(32)
        # int.from_bytes returns 0..2**256-1; we must skip 0 and >= n
        value = int.from_bytes(candidate, "big")
        if 0 < value < _SECP256K1_N:
            return candidate


def derive_eth_address(public_key_uncompressed: bytes) -> str:
    """
    Convert an uncompressed Ethereum public key (64 bytes, X||Y) to an EIP-55 address.
    """
    if len(public_key_uncompressed) != 64:
        raise ValueError("Ethereum public key must be 64 bytes (X || Y) without prefix")
    address_bytes = keccak(public_key_uncompressed)[-20:]
    return to_checksum_address(address_bytes)


def generate_eth_keypair(rng: SupportsGetBytes | HashStreamRNG | None = None) -> EthKeyMaterial:
    """
    Generate a random Ethereum private key, derive the corresponding public key and address.

    Parameters
    ----------
    rng:
        Optional source of randomness implementing ``get_bytes``. If not provided,
        a new HashStreamRNG seeded from os.urandom will be instantiated.
    """
    if rng is None:
        rng = HashStreamRNG.from_seed_components(None)

    private_key_bytes = _generate_private_key_bytes(rng)
    priv = PrivateKey(private_key_bytes)
    pub_uncompressed = priv.public_key.format(compressed=False)[1:]  # drop 0x04 prefix
    address = derive_eth_address(pub_uncompressed)
    return EthKeyMaterial(
        private_key=private_key_bytes,
        public_key=pub_uncompressed,
        address=address,
    )
