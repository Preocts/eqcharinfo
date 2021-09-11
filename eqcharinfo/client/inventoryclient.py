"""Reads in an Everquest /inventory file"""
import csv
import logging
from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional

from eqcharinfo.models.inventory import Inventory


class InventoryClient:
    """Reads in an Everquest inventory file"""

    log = logging.getLogger(__name__)

    def __init__(self, filepath: str, character_name: Optional[str] = None) -> None:
        """Loads inventory file. If character name is excluded, filename is used"""
        self._filepath = Path(filepath).resolve()
        self._name = self._filepath.name if character_name is None else character_name
        self._inventories: List[Inventory] = []

    def __iter__(self) -> Generator[Inventory, None, None]:
        """Iterate over inventories"""
        for inventory in self._inventories:
            yield inventory

    @property
    def name(self) -> str:
        """Character name for the inventory"""
        return self._name

    @property
    def inventories(self) -> List[Inventory]:
        """List of Inventory objects loaded"""
        return self._inventories.copy()

    def load_file(self) -> None:
        """Populates inventory from file in instance's filepath attribute"""
        self.log.info("Loading inventory file `%s`", self._filepath)

        with self._filepath.open(mode="r", encoding="utf-8") as infile:
            dictreader = csv.DictReader(infile, delimiter="\t")
            for row in dictreader:
                self._inventories.append(
                    Inventory(
                        location=row["Location"],
                        name=row["Name"],
                        id=int(row["ID"]),
                        count=int(row["Count"]),
                        slots=int(row["Slots"]),
                    )
                )
