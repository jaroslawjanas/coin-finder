from __future__ import annotations

import asyncio
from datetime import timedelta

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from coin_finder.pipeline.stats import Statistics, StatsSnapshot


def _format_duration(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))


def _build_summary_table(snapshot: StatsSnapshot) -> Table:
    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="right", ratio=1)

    table.add_row("Uptime", _format_duration(snapshot.uptime))
    table.add_row("Total Batches", f"{snapshot.total_batches:,}")
    table.add_row("Total Keys", f"{snapshot.total_keys_generated:,}")
    table.add_row("Total Requests", f"{snapshot.total_requests:,}")
    table.add_row("Hits Found", f"{snapshot.total_hits:,}")
    table.add_row("Errors", f"{snapshot.total_errors:,}")
    table.add_row("Last Batch Duration", f"{snapshot.last_batch_duration_ms:.1f} ms")
    table.add_row("Last RPC Latency", f"{snapshot.last_rpc_latency_ms:.1f} ms")
    table.add_row("Last Hit", snapshot.last_hit or "—")

    return table


def _build_rate_table(snapshot: StatsSnapshot) -> Table:
    table = Table(title="Throughput", expand=True, box=box.SIMPLE, show_header=False)
    table.add_column("metric", justify="left")
    table.add_column("value", justify="right")
    table.add_row("Requests/sec", f"{snapshot.requests_per_sec:,.2f}")
    table.add_row("Keys/sec", f"{snapshot.keys_per_sec:,.2f}")
    table.add_row("Hits/sec", f"{snapshot.hits_per_sec:,.6f}")
    return table


async def dashboard_loop(
    stats: Statistics,
    stop_event: asyncio.Event,
    *,
    refresh_interval: float = 0.25,
    console: Console | None = None,
) -> None:
    console = console or Console()
    layout = Layout()
    layout.split(
        Layout(name="summary", ratio=2),
        Layout(name="rates", ratio=1),
    )

    refresh_hz = None
    if refresh_interval > 0:
        refresh_hz = max(1, int(1 / refresh_interval))
    with Live(
        layout,
        refresh_per_second=refresh_hz,
        console=console,
        vertical_overflow="visible",
    ):
        while not stop_event.is_set():
            snapshot = await stats.snapshot()
            layout["summary"].update(
                Panel(
                    _build_summary_table(snapshot),
                    title="coin-finder :: Ethereum Scan",
                    border_style="cyan",
                )
            )
            layout["rates"].update(
                Panel(
                    _build_rate_table(snapshot),
                    title="Rates",
                    border_style="magenta",
                )
            )
            if refresh_interval <= 0:
                await stop_event.wait()
            else:
                await asyncio.sleep(refresh_interval)
