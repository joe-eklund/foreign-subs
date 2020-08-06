"""Run fsubs app."""
import inspect
import logging
import pathlib
from collections import defaultdict
from enum import Enum
from pathlib import Path

import typer
import uvicorn

from fsubs.config.config import Config

ROOTLOGGER = logging.getLogger(inspect.getmodule(__name__))
LOGGER = logging.getLogger(__name__)
LOG_FORMAT = "%(asctime)s - %(name)s:%(funcName)s:%(lineno)s - " \
             "%(levelname)s - %(message)s"

cli = typer.Typer(add_completion=False)
config = Config()


class LogLevel(str, Enum):
    """Available log levels."""

    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class JWTAlgorithm(str, Enum):
    """
    Available jwt algorithms.

    Taken from: https://pyjwt.readthedocs.io/en/latest/algorithms.html#digital-signature-algorithms
    """

    HS256 = "HS256"  # HMAC using SHA-256 hash algorithm (default)
    HS384 = "HS384"  # HMAC using SHA-384 hash algorithm
    HS512 = "HS512"  # HMAC using SHA-512 hash algorithm
    ES256 = "ES256"  # ECDSA signature algorithm using SHA-256 hash algorithm
    ES384 = "ES384"  # ECDSA signature algorithm using SHA-384 hash algorithm
    ES512 = "ES512"  # ECDSA signature algorithm using SHA-512 hash algorithm
    RS256 = "RS256"  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-256 hash algorithm
    RS384 = "RS384"  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-384 hash algorithm
    RS512 = "RS512"  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-512 hash algorithm
    PS256 = "PS256"  # RSASSA-PSS signature using SHA-256 and MGF1 padding with SHA-256
    PS384 = "PS384"  # RSASSA-PSS signature using SHA-384 and MGF1 padding with SHA-384
    PS512 = "PS512"  # RSASSA-PSS signature using SHA-512 and MGF1 padding with SHA-512


def setup_logging():
    """Set up logging based on provided log params."""
    formatter = logging.Formatter(LOG_FORMAT)
    ROOTLOGGER.setLevel(config["app"]["log_level"].upper())

    sh = logging.StreamHandler()
    sh.setLevel(config["app"]["log_level"].upper())
    sh.setFormatter(formatter)
    ROOTLOGGER.addHandler(sh)

    LOGGER.info("-------------------------STARTING-------------------------")
    LOGGER.info("INFO Logging Level -- Enabled")
    LOGGER.warning("WARNING Logging Level -- Enabled")
    LOGGER.critical("CRITICAL Logging Level -- Enabled")
    LOGGER.debug("DEBUG Logging Level -- Enabled")


@cli.command()
def main(
    base_url: str = typer.Option(None, help="Set the base url used by fsubs."),
    bind_address: str = typer.Option(None, help="Set application bind IP address."),
    bind_port: int = typer.Option(None, help="Set app bind port."),
    cfg: Path = typer.Option("", "--config", "-c", help="Load a custom config file."),
    jwt_algorithm: JWTAlgorithm = typer.Option(
        None,
        help="Set the jwt algorithm used to encode tokens. Default to HS256."),
    jwt_expires_hours: int = typer.Option(None, help="Set jwt expiration in hours."),
    jwt_secret: str = typer.Option(None, help="Set the jwt secret used to encode/decode."),
    log_level: LogLevel = typer.Option(None, "--log-level", "-l", help="Set the log level. Default"
                                                                       " to info."),
    db_hostname: str = typer.Option(None, help="Set the database hostname."),
    db_password: str = typer.Option(None, help="Set the database password."),
    db_port: int = typer.Option(None, help="Set the database port."),
    db_username: str = typer.Option(None, help="Set the database username."),

):
    """Run fsubs backend."""
    LOGGER.debug(f"Loading config from {cfg}.")
    config.read(cfg)
    cli_args = defaultdict(dict)
    cli_args["app"]["base_url"] = base_url
    cli_args["app"]["bind_address"] = bind_address
    cli_args["app"]["bind_port"] = bind_port
    cli_args["app"]["jwt_algorithm"] = jwt_algorithm
    cli_args["app"]["jwt_expires_hours"] = jwt_expires_hours
    cli_args["app"]["jwt_secret"] = jwt_secret
    if log_level is not None:
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
    setup_logging()
    uvicorn.run(
        app='fsubs.routers.main:app',
        host=config["app"]["bind_address"],
        port=config["app"].getint("bind_port"),
        reload=config["app"].getboolean("reload"),
        reload_dirs=[pathlib.Path(__file__).parent.absolute()],
        log_level=config["app"]["log_level"],
    )


if __name__ == "__main__":
    cli()
