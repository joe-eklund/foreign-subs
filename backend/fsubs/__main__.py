"""Run fsubs app."""

from enum import Enum
import logging
from pathlib import Path

import typer
import uvicorn

from fsubs.routers.api import app
from fsubs.config.config import config


logger = logging.getLogger(__name__)

cli = typer.Typer(add_completion=False)


class LogLevel(str, Enum):
    """Available log levels."""

    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


@cli.command()
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
    uvicorn.run(
        app,
        host=config["app"]["bind_addr"],
        port=config["app"].getint("bind_port"),
        reload=True)


if __name__ == "__main__":
    cli()
