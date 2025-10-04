from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class AppConfig:
    eth_rpc_url: str
    provider_name: str = "ethereum"
    workers: int = 4
    batch_size: int = 512
    rpc_timeout: float = 30.0
    rpc_max_outstanding_requests: int = 8
    output_dir: Path = Path("output")
    hits_filename: str = "eth_hits.csv"
    stats_refresh_interval: float = 0.25
    seed: Optional[str] = None
    log_level: str = "INFO"

    @property
    def hits_path(self) -> Path:
        return self.output_dir / self.hits_filename
