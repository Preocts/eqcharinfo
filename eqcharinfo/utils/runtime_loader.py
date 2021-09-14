"""
Used to manage all run-time setup operations
"""
import contextlib
import logging
import os
import sqlite3
from configparser import ConfigParser
from sqlite3 import Connection
from typing import Generator

EQCHARINFO_LOG = os.getenv("EQCHARINFO_LOG", "DEBUG")
EQCHARDATABASE = os.getenv("EQCHARDATABASE", "eqcharinfo.sqlite3")

log = logging.getLogger(__name__)


def add_logger() -> None:
    """Set a logger, overrides root handlers if already set"""
    logging.basicConfig(format="%(asctime)s %(message)s", level=EQCHARINFO_LOG)


def load_config() -> ConfigParser:
    """Loads default config file or file set by EQCHARINFO_CONFIG"""
    config = ConfigParser()

    files = config.read(os.getenv("EQCHARINFO_CONFIG", "appsettings.ini"))

    log.info("Loaded the following config file(s): %s", files)

    return config


@contextlib.contextmanager
def load_database(database: str = EQCHARDATABASE) -> Generator[Connection, None, None]:
    """
    Connect to sqlite3 database, ensures connection is closed with context manager

    Common Use:
        with load_database() as dbconnection:
            ...
    """
    try:
        connection = sqlite3.connect(database=database)
        yield connection

    finally:
        connection.close()
