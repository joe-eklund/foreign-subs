"""Run fsubs app."""

import logging
from collections import defaultdict
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
    base_url: str = typer.Option(None, help="Set the base url used by fsubs."),
    bind_address: str = typer.Option(None, help="Set application bind IP address."),
    bind_port: int = typer.Option(None, help="Set app bind port."),
    cfg: Path = typer.Option("", "--config", "-c", help="Load a custom config file."),
    db_hostname: str = typer.Option(None, help="Set the database hostname."),
    db_password: str = typer.Option(None, help="Set the database password."),
    db_port: int = typer.Option(None, help="Set the database port."),
    db_username: str = typer.Option(None, help="Set the database username."),
    log_level: LogLevel = typer.Option(
        LogLevel.info.value, "--log-level", "-l", show_default=True
    ),
):
    """Run fsubs backend."""
    LOGGER.debug(f"Loading config from {cfg}.")
    config.read(cfg)

    cli_args = defaultdict(dict)
    cli_args["app"]["bind_address"] = bind_address
    cli_args["app"]["bind_port"] = bind_port
    cli_args["app"]["base_url"] = base_url
    cli_args["app"]["log_level"] = log_level.value
    cli_args["db"]["hostname"] = db_hostname
    cli_args["db"]["port"] = db_port
    cli_args["db"]["username"] = db_username
    cli_args["db"]["password"] = db_password

    actual_args = defaultdict(dict)
    for name, section in cli_args.items():
        for key, value in section.items():
            if value is not None:
                actual_args[name][key] = value
    config.read_dict(vars=actual_args)

    if config["app"]["base_url"] and not config["app"]["base_url"].startswith("/"):
        config["app"]["base_url"] = f'/{config["app"]["base_url"]}'

    uvicorn.run(
        app='fsubs.routers.main:app',
        host=config["app"]["bind_addr"],
        port=config["app"].getint("bind_port"),
        reload=config["app"].getboolean("reload"),
        log_level=config["app"]["log_level"],
    )


if __name__ == "__main__":
    cli()
