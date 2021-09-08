"""
Used to manage all run-time setup operations
"""
import logging
import os
from configparser import ConfigParser
from pathlib import Path

EQCHARINFO_LOG = os.getenv("EQCHARINFO_LOG", "DEBUG")

log = logging.getLogger(__name__)


def set_logger(name: str, level: str = EQCHARINFO_LOG) -> logging.Logger:
    """Set a logger, overrides root handlers if already set"""
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    logging.basicConfig(format="%(asctime)s %(message)s", level=level)

    return logging.getLogger(name)


def load_config() -> ConfigParser:
    """Loads default config file or file set by EQCHARINFO_ENV"""
    env = os.getenv("EQCHARINFO_ENV", "")
    ini_list = [
        (Path(__file__).parent / "../../appsetting.ini").resolve(),
        (Path(__file__).parent / f"../../appsetting-{env}").resolve(),
    ]

    config = ConfigParser()

    files = config.read(ini_list)

    log.info("Loaded the following config file(s): %s", files)

    return config
