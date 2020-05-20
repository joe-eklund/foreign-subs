"""Configure fsubs app."""

import pathlib
from collections import defaultdict
from configparser import ConfigParser
from os import environ


VAR_PREFIX = "FSUBS"


class Config:
    """Config singleton class."""

    _instance = None

    def __new__(cls):
        """Implement singleton pattern."""
        if Config._instance is None:
            Config._instance = object.__new__(cls)
            Config._instance.config = ConfigParser()
            with open(f"{pathlib.Path(__file__).parent.absolute()}/default.ini") as f:
                Config._instance.config.read_file(f)
            Config._instance.config.read(
                f"{pathlib.Path(__file__).parent.absolute()}/default_reload.ini")
        return Config._instance

    def read(self, cfg_file):
        """Add a new config file."""
        self.config.read(cfg_file)

    def read_dict(self, vars):
        """Add environment variables to config."""
        self.config.read_dict(vars)

    def __getitem__(self, key):
        """
        Get the section in the ``Config`` object with the given key.

        :param: The key to the entry to get.
        :returns: The entry of the given key.
        """
        return self.config[key]

    def __delitem__(self, key):
        """
        Delete the section in this ``Config`` object with the given key.

        :param key: The key of the key-value pair to delete.
        """
        self.config.remove_section(key)

    def __repr__(self):
        """
        Return the string representation of a ``Config`` object.

        :returns: The string representation of a ``Config`` object.
        """
        return str({name: dict(section) for name, section in self.config.items()})


def get_env_vars():
    """Read environment variables to a dict."""
    vars = defaultdict(dict)
    names = [
        "APP_BIND_ADDRESS",
        "APP_BIND_PORT",
        "APP_BASE_URL",
        "APP_LOG_LEVEL",
        "DB_HOSTNAME",
        "DB_PASSWORD",
        "DB_PORT",
        "DB_USERNAME",
    ]
    for name in names:
        try:
            section, key = name.lower().split("_", 1)
            vars[section][key] = environ[f"{VAR_PREFIX}_{name}"]
        except KeyError:
            pass
    return vars
