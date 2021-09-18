"""Read and provides access to a Character's Inventory objects"""
import csv
import logging
from io import StringIO
from pathlib import Path
from typing import Dict
from typing import Generator
from typing import List

from eqcharinfo.models.inventory import Inventory
from eqcharinfo.utils import fuzzy_search


class CharacterInventoryClient:
    """Read and provides access to a Character's Inventory objects"""

    log = logging.getLogger(__name__)

    def __init__(self, character_name: str) -> None:
        """Creates an empty instance"""
        self._character_name = character_name
        self._inventory: Dict[str, Inventory] = {}

    def __iter__(self) -> Generator[Inventory, None, None]:
        """Iterate through inventory"""
        for item in self._inventory.values():
            yield item

    @property
    def character_name(self) -> str:
        return self._character_name

    @property
    def inventory(self) -> List[Inventory]:
        return list(self._inventory.values())

    def search(self, search_string: str, max_results: int = 50) -> List[Inventory]:
        """Searches a character's inventory"""
        search_items = {inv.name: inv.id for inv in self._inventory.values()}
        result = fuzzy_search.search(search_string, search_items, max_results)
        found: List[Inventory] = []
        for id in result.values():
            found.extend([slot for slot in self._inventory.values() if slot.id == id])
        return found

    def load_from_file(self, filepath: str) -> None:
        """Populates inventory of character from filepath"""
        path = Path(filepath).resolve()
        self.log.info("Loading inventory file `%s`", path)
        with path.open(mode="r", encoding="utf-8") as infile:
            dictreader = csv.DictReader(infile, delimiter="\t")
            self._dictreader_to_inventory(dictreader)

    def load_from_string(self, string: str) -> None:
        """Populates inventory of character from string"""
        filelike = StringIO(string)
        self.log.info("Loading inventory file from string. Len: %d", len(string))
        dictreader = csv.DictReader(filelike, delimiter="\t")
        self._dictreader_to_inventory(dictreader)

    def _dictreader_to_inventory(self, dictreader: csv.DictReader) -> None:  # type: ignore # noqa:E501
        """Internal Use: translates dictreader to Inventory objects"""
        for row in dictreader:
            if row["Name"] == "Empty":
                continue
            self._inventory[row["Location"]] = Inventory(
                location=row["Location"],
                name=row["Name"],
                id=row["ID"],
                count=row["Count"],
                slots=row["Slots"],
            )
