"""Client for accessing Lucy item data"""
import csv
import gzip
import logging
from pathlib import Path
from typing import Generator
from typing import List

from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.utils.fileutil import most_recent


class LucyItemClient:
    """Lucy Item data client"""

    # TODO: These should be from config file
    FILE_PATTERN = "*txt.gz"
    FILE_DIR = "../downloads"

    log = logging.getLogger(__name__)

    def __init__(self) -> None:
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
        self._load(Path(most_recent(self.FILE_DIR, self.FILE_PATTERN)))

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
