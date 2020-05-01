"""Run fsubs app."""

import logging
from enum import Enum
from pathlib import Path

import typer
import uvicorn

from fsubs.config.config import config


LOGGER = logging.getLogger(__name__)

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
    ),
    reload: bool = typer.Option(
        False, "--reload", "-r", help="Auto reload on code changes.", show_default=True),
):
    """Run fsubs backend."""
    LOGGER.debug(f"Loading config from {cfg}.")
    config.read(cfg)
    uvicorn.run(
        app='fsubs.routers.api:app',
        host=config["app"]["bind_addr"],
        port=config["app"].getint("bind_port"),
        reload=reload,
        log_level=log_level,
    )


if __name__ == "__main__":
    cli()
