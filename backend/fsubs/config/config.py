"""Configure fsubs app."""
import pathlib
from configparser import ConfigParser

config = ConfigParser()


config.read(f"{pathlib.Path(__file__).parent.absolute()}/default.ini")
