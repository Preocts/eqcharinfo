"""Read and provides access to Character Inventory objects"""
import csv
import logging
from io import StringIO
from pathlib import Path
from typing import Dict
from typing import List

from eqcharinfo.models.inventory import Inventory

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
            self._char_inventories[character_name][row["Location"]] = Inventory(
                location=row["Location"],
                name=row["Name"],
                id=row["ID"],
                count=row["Count"],
                slots=row["Slots"],
            )
