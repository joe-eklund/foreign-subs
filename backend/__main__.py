"""Run fsubs app."""

from enum import Enum
import logging
from pathlib import Path

import typer
import uvicorn

from backend.routers.api import app
from backend.config.config import config


logger = logging.getLogger(__name__)


class LogLevel(str, Enum):
    """Available log levels."""

    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


def main(
    cfg: Path = typer.Option("", "--config", "-c", help="Load a custom config file."),
    log_level: LogLevel = typer.Option(
        LogLevel.warning.value, "--log-level", "-l", show_default=True
    )
):
    """Run fsubs backend."""
    logging.basicConfig(level=log_level.upper())
    logger.debug(f"Loading config from {cfg}.")
    config.read(cfg)
    uvicorn.run(app, host=config["app"]["bind_addr"], port=config["app"].getint("bind_port"))


if __name__ == "__main__":
    typer.run(main)
