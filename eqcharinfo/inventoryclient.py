"""Reads in an Everquest /inventory file"""
import csv
import logging
from io import StringIO
from pathlib import Path
from typing import Dict
from typing import Generator

from eqcharinfo.models.inventory import Inventory


class InventoryClient:
    """Parses an EverQuest character inventory file"""

    log = logging.getLogger(__name__)

    def __init__(self, character_name: str) -> None:
        """Loads inventory file. If character name is excluded, filename is used"""
        self.character_name = character_name
        self.inventories: Dict[str, Inventory] = {}

    def __iter__(self) -> Generator[Inventory, None, None]:
        """Iterate over inventories"""
        for inventory in self.inventories.values():
            yield inventory

    def load_from_file(self, filepath: str) -> None:
        """Populates inventory from filepath"""
        path = Path(filepath).resolve()
        self.log.info("Loading inventory file `%s`", path)
        with path.open(mode="r", encoding="utf-8") as infile:
            dictreader = csv.DictReader(infile, delimiter="\t")
            self._dictreader_to_inventory(dictreader)

    def load_from_string(self, string: str) -> None:
        """Populates inventory from string"""
        filelike = StringIO(string)
        self.log.info("Loading inventory file from string. Len: %d", len(string))
        dictreader = csv.DictReader(filelike, delimiter="\t")
        self._dictreader_to_inventory(dictreader)

    def _dictreader_to_inventory(
        self,
        dictreader: csv.DictReader,  # type: ignore
    ) -> None:
        """Internal Use: translates dictreader to Inventory objects"""
        for row in dictreader:
            self.inventories[row["Location"]] = Inventory(
                location=row["Location"],
                name=row["Name"],
                id=row["ID"],
                count=row["Count"],
                slots=row["Slots"],
            )
