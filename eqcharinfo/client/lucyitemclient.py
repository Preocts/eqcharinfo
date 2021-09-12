"""Client for accessing Lucy item data"""
import csv
import gzip
import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Generator
from typing import List

from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.utils.fileutil import most_recent


class LucyItemClient:
    """Lucy Item data client"""

    log = logging.getLogger(__name__)

    def __init__(self, config: ConfigParser) -> None:
        self.file_dir = config["DOWNLOAD-ITEMFILE"]["download_path"]
        self.file_pattern = config["DOWNLOAD-ITEMFILE"]["glob_pattern"]
        self._lucyitems: List[LucyItem] = []

    def __iter__(self) -> Generator[LucyItem, None, None]:
        for lucyitem in self._lucyitems:
            yield lucyitem

    @property
    def lucyitems(self) -> List[LucyItem]:
        """List of loaded items, can be empty"""
        return self._lucyitems.copy()

    def load_from_file(self, filepath: str) -> None:
        """Loads item data from specific file"""
        self._load(Path(filepath).resolve())

    def load_from_recent(self) -> None:
        """Loads from most recent item data file available"""
        self._load(Path(most_recent(self.file_dir, self.file_pattern)))

    def _load(self, filepath: Path) -> None:
        """Private: Loads item data from Path given"""

        self.log.info("Unpacking and loading `%s`", filepath)

        with gzip.open(filepath, "rt") as infile:
            dictreader = csv.DictReader(infile)

            for row in dictreader:
                self._lucyitems.append(
                    LucyItem(
                        id=int(row["id"]),
                        name=row["name"],
                        lucylink=row["lucylink"],
                    )
                )
