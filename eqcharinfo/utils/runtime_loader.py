"""
Used to manage all run-time setup operations
"""
import logging
import os
from configparser import ConfigParser
from typing import Optional


class RuntimeLoader:
    """Manage run-time setup operations"""

    EQCHARINFO_LOG = os.getenv("EQCHARINFO_LOG", "DEBUG")

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.config: Optional[ConfigParser] = None

    def add_logger(self) -> None:
        """Set a logger, overrides root handlers if already set"""
        logging.basicConfig(format="%(asctime)s %(message)s", level=self.EQCHARINFO_LOG)

    def load_config(self) -> None:
        """Loads default config file or file set by EQCHARINFO_CONFIG"""
        self.config = ConfigParser()
        files = self.config.read(os.getenv("EQCHARINFO_CONFIG", "appsettings.ini"))
        self.log.info("Loaded the following config file(s): %s", files)

    def get_config(self) -> ConfigParser:
        """Returns config"""
        if self.config is None:
            self.load_config()

        return self.config  # type: ignore
