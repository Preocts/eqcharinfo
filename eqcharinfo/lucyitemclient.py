"""Client for accessing Lucy item data"""
import csv
import gzip
import logging
from configparser import SectionProxy
from pathlib import Path
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.utils.fileutil import most_recent


class LucyItemClient:
    """Lucy Item data client"""

    log = logging.getLogger(__name__)

    def __init__(self, config_section: SectionProxy) -> None:
        self.file_dir = config_section.get("file_path", "")
        self.file_pattern = config_section.get("glob_pattern", "")
        self._lucyitems: Dict[str, LucyItem] = {}

    def __iter__(self) -> Generator[LucyItem, None, None]:
        for lucyitem in [value for value in self._lucyitems.values()]:
            yield lucyitem

    @property
    def lucyitems(self) -> List[LucyItem]:
        """List of loaded items, can be empty"""
        return [value for value in self._lucyitems.values()]

    def get_by_id(self, id: str) -> Optional[LucyItem]:
        """Get an item by id, returns None if not found"""
        return self._lucyitems.get(id)

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
                self._lucyitems[row["id"]] = LucyItem(
                    id=row["id"],
                    name=row["name"],
                    lucylink=row["lucylink"],
                )
