"""Download Lucy item files and handle housekeeping on them"""
import logging
import os
from configparser import SectionProxy
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import requests


class LucyItemFileManager:
    """Download Lucy item files and handle housekeeping on them"""

    def __init__(self, config_section: SectionProxy) -> None:
        """
        Download Lucy item files and handle housekeeping

        Args:
            config_section: A SectionProxy containing the following:
                url : URL of where to download the item file
                glob_pattern : filepattern to identify downloaded files
                file_path : Where to store downloaded files
                file_name : strftime formatted naming scheme
                retain_for_days : Number of days, per file, before deleting file
        """
        self.log = logging.getLogger(__name__)

        filename_format = config_section["file_name"]

        self.url = config_section["url"]
        self.file_path = Path(config_section["file_path"]).resolve()
        self.fullfile_path = self.file_path / datetime.now().strftime(filename_format)
        self.retain_for_days = int(config_section["retain_for_days"])
        self.glob_pattern = config_section["glob_pattern"]

    def housekeeping(self) -> None:
        """Creates needed directories, cleans up extra downloads by retention period"""

        self.file_path.mkdir(exist_ok=True)
        expiry = datetime.now() - timedelta(days=self.retain_for_days)

        # Old gz file cleanup
        for file in self.file_path.glob(self.glob_pattern):
            created = datetime.fromtimestamp(os.path.getctime(file))
            if expiry > created:
                os.remove(file)

    def download_itemlist(self) -> None:
        """Downloads the Lucy itemlist, saves to given filepath"""

        if self.fullfile_path.exists():
            self.log.info("Version exists, skipping download '%s'", self.fullfile_path)
            return

        self.log.debug("Downloading itemlist from '%s'", self.url)

        with requests.get(self.url, stream=True) as request:
            request.raise_for_status()
            with open(self.fullfile_path, "wb") as fileout:
                for chunk in request.iter_content(chunk_size=8192):
                    fileout.write(chunk)

        self.log.info("File saved as '%s'", self.fullfile_path)
