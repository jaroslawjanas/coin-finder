from __future__ import annotations

import logging
import sys
from typing import Any

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def _resolve_level(level: str | int | None) -> int:
    if isinstance(level, int):
        return level
    if isinstance(level, str):
        try:
            return logging.getLevelName(level.upper())  # type: ignore[arg-type]
        except (AttributeError, ValueError):
            pass
    return logging.INFO


def configure_logging(level: str | int | None = logging.INFO, *, disable_existing: bool = False) -> None:
    logging.basicConfig(
        level=_resolve_level(level),
        format=_LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=disable_existing,
    )
