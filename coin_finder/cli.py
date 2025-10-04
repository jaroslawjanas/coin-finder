from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv

from coin_finder.config import AppConfig
from coin_finder.pipeline.runner import run

load_dotenv()

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _validate_positive(value: int, name: str) -> int:
    if value <= 0:
        raise typer.BadParameter(f"{name} must be positive")
    return value


@app.command("scan", help="Run continuous Ethereum address scanning workers.")
def scan(
    eth_rpc_url: str = typer.Option(
        ...,
        "--eth-rpc-url",
        envvar="ETH_RPC_URL",
        help="Ethereum JSON-RPC endpoint supporting batch eth_getBalance calls.",
    ),
    provider_name: str = typer.Option(
        "ethereum",
        "--provider-name",
        envvar="PROVIDER_NAME",
        help="Identifier stored in CSV output (default: ethereum).",
    ),
    workers: int = typer.Option(
        4,
        "--workers",
        "-w",
        envvar="WORKERS",
        callback=lambda value: _validate_positive(value, "workers"),
        help="Number of concurrent worker tasks.",
    ),
    batch_size: int = typer.Option(
        512,
        "--batch-size",
        "-b",
        envvar="BATCH_SIZE",
        callback=lambda value: _validate_positive(value, "batch-size"),
        help="Number of private keys generated per worker batch.",
    ),
    rpc_timeout: float = typer.Option(
        30.0,
        "--rpc-timeout",
        envvar="RPC_TIMEOUT",
        help="HTTP timeout (seconds) for RPC requests.",
    ),
    rpc_max_outstanding_requests: int = typer.Option(
        8,
        "--rpc-max-outstanding",
        envvar="RPC_MAX_OUTSTANDING",
        callback=lambda value: _validate_positive(value, "rpc-max-outstanding"),
        help="Maximum concurrent RPC requests.",
    ),
    stats_refresh_interval: float = typer.Option(
        0.25,
        "--stats-refresh-interval",
        envvar="STATS_REFRESH_INTERVAL",
        help="Dashboard refresh interval in seconds.",
    ),
    output_dir: Path = typer.Option(
        Path("output"),
        "--output-dir",
        envvar="OUTPUT_DIR",
        help="Directory for CSV hit outputs.",
    ),
    hits_filename: str = typer.Option(
        "eth_hits.csv",
        "--hits-filename",
        envvar="HITS_FILENAME",
        help="Filename for the hits CSV within the output directory.",
    ),
    seed: Optional[str] = typer.Option(
        None,
        "--seed",
        envvar="SEED",
        help="Optional base seed mixed with timestamps for RNG determinism.",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        envvar="LOG_LEVEL",
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    ),
) -> None:
    config = AppConfig(
        eth_rpc_url=eth_rpc_url,
        provider_name=provider_name,
        workers=workers,
        batch_size=batch_size,
        rpc_timeout=rpc_timeout,
        rpc_max_outstanding_requests=rpc_max_outstanding_requests,
        output_dir=output_dir,
        hits_filename=hits_filename,
        stats_refresh_interval=stats_refresh_interval,
        seed=seed,
        log_level=log_level,
    )
    run(config)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
