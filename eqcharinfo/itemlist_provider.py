"""
Downloads and maintains existing downloads (cleanup) of Lucy's itemlist
"""
import logging
import os
from configparser import SectionProxy
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import requests


class ItemListProvider:
    """Downloads and maintains existing downloads of Lucy's itemlist"""

    def __init__(self, config: SectionProxy) -> None:
        """Creates a provider instance"""
        self.log = logging.getLogger(__name__)
        self.config = config
        filename_format = self.config.get("filename", "undefined")
        self.dir_path = Path(self.config.get("file_path", "")).resolve()
        self.file_url = self.config.get("url", "")
        self.file_path = self.dir_path / datetime.now().strftime(filename_format)

    def housekeeping(self) -> None:
        """Housekeeping of directories and paths, cleans up extra backups"""

        self.dir_path.mkdir(exist_ok=True)
        expiry = datetime.now() - timedelta(days=self.config.getint("keep_for_days"))

        # Old gz file cleanup
        for file in self.dir_path.glob("*txt.gz"):
            created = datetime.fromtimestamp(os.path.getctime(file))
            if expiry > created:
                os.remove(file)

    def download_itemlist(self) -> None:
        """Downloads the Lucy itemlist, saves to given filepath"""

        if self.file_path.exists():
            self.log.info("Version exists, skipping download '%s'", self.file_path)
            return

        self.log.debug("Downloading itemlist from '%s'", self.file_url)

        with requests.get(self.file_url, stream=True) as request:
            request.raise_for_status()
            with open(self.file_path, "wb") as fileout:
                for chunk in request.iter_content(chunk_size=8192):
                    fileout.write(chunk)

        self.log.info("File saved as '%s'", self.file_path)
