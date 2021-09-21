"""Provides access to Lucy Item objects from file"""
import csv
import gzip
import logging
from configparser import SectionProxy
from pathlib import Path
from typing import Generator
from typing import Optional

from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.utils.fileutil import most_recent


class LucyItemProvider:
    """Provides access to Lucy Item objects from file"""

    def __init__(self, config_section: SectionProxy) -> None:
        """
        Creates provider for loading and accessing LucyItem objects

        Args:
            config_section: A SectionProxy containing the following:
                glob_pattern : filepattern to identify downloaded file
                file_path : Where to store downloaded files
        """
        self.log = logging.getLogger(__name__)
        self.glob_pattern = config_section["glob_pattern"]
        self.file_path = config_section["file_path"]
        self._lucyitems: dict[str, LucyItem] = {}

    def __iter__(self) -> Generator[LucyItem, None, None]:
        """Allow iteration through provider"""
        for item in self._lucyitems.values():
            yield item

    def __len__(self) -> int:
        """Return # of loaded items"""
        return len(self._lucyitems)

    @property
    def lucyitems(self) -> list[LucyItem]:
        """Returns list of LucyItems"""
        return list(self._lucyitems.values())

    def get_by_id(self, item_id: str) -> Optional[LucyItem]:
        """Returns by id or returns None"""
        return self._lucyitems.get(item_id)

    def load_from_file(self, filepath: str) -> None:
        """Loads item data from specific file"""
        self._load(Path(filepath).resolve())

    def load_from_recent(self) -> None:
        """Loads from most recent item data file available"""
        self._load(Path(most_recent(self.file_path, self.glob_pattern)))

    def _load(self, filepath: Path) -> None:
        """Private: Loads item data from Path given"""

        self.log.info("Unpacking and loading `%s`", filepath)

        with gzip.open(filepath, "rt") as infile:
            dictreader = csv.DictReader(infile)

            for row in dictreader:
                self._lucyitems[row["id"]] = LucyItem(
                    id=row["id"],
                    name=row["name"],
                    lucylink=row["lucylink"],
                )
