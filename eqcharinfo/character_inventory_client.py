"""Read and provides access to Character Inventory objects"""
import csv
import logging
from io import StringIO
from pathlib import Path
from typing import Dict
from typing import List

from eqcharinfo.models.inventory import Inventory
from eqcharinfo.utils import fuzzy_search

CHARINV = Dict[str, Dict[str, Inventory]]


class CharacterInventoryClient:
    """Read and provides access to Character Inventory objects"""

    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """Creates an empty instance"""
        self._char_inventories: CHARINV = {}

    def get_character(self, character_name: str) -> List[Inventory]:
        """Returns list of inventory objects for a given character, can be empty"""
        return list(self._char_inventories.get(character_name, {}).values())

    def search_character(
        self, character_name: str, search_string: str, max_results: int = 10
    ) -> List[Inventory]:
        """Searches a character's inventory"""
        char_slots = self._char_inventories.get(character_name, {})
        search_items = {inv.name: inv.id for inv in char_slots.values()}
        result = fuzzy_search.search(search_string, search_items, max_results)
        found: List[Inventory] = []
        for itemid in result.values():
            found.extend([slot for slot in char_slots.values() if slot.id == itemid])
        return found

    def load_from_file(self, filepath: str, character_name: str) -> None:
        """Populates inventory of character from filepath"""
        path = Path(filepath).resolve()
        self.log.info("Loading inventory file `%s`", path)
        with path.open(mode="r", encoding="utf-8") as infile:
            dictreader = csv.DictReader(infile, delimiter="\t")
            self._dictreader_to_inventory(dictreader, character_name)

    def load_from_string(self, string: str, character_name: str) -> None:
        """Populates inventory of character from string"""
        filelike = StringIO(string)
        self.log.info("Loading inventory file from string. Len: %d", len(string))
        dictreader = csv.DictReader(filelike, delimiter="\t")
        self._dictreader_to_inventory(dictreader, character_name)

    def _dictreader_to_inventory(
        self, dictreader: csv.DictReader, character_name: str  # type: ignore
    ) -> None:
        """Internal Use: translates dictreader to Inventory objects"""
        self._char_inventories[character_name] = {}
        for row in dictreader:
            if row["Name"] == "Empty":
                continue
            self._char_inventories[character_name][row["Location"]] = Inventory(
                location=row["Location"],
                name=row["Name"],
                id=row["ID"],
                count=row["Count"],
                slots=row["Slots"],
            )
