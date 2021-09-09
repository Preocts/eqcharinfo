"""Reads in an Everquest /inventory file"""
import csv
import logging
from pathlib import Path
from typing import List
from typing import Optional

from eqcharinfo.models.inventory import Inventory


class InventoryClient:
    """Reads in an Everquest inventory file"""

    log = logging.getLogger(__name__)

    def __init__(self, filepath: str, name: Optional[str] = None) -> None:
        """Loads inventory file. If name is excluded, filename is used"""
        self.filepath = Path(filepath).resolve()
        self.name = self.filepath.name if name is None else name
        self._raw_file = ""
        self._inventory: List[Inventory] = []

        self.load_file()

    def load_file(self) -> None:
        """Loads a file"""
        self.log.info("Loading inventory file `%s`", self.filepath)

        with self.filepath.open(mode="r", encoding="utf-8") as infile:
            dictreader = csv.DictReader(infile, delimiter="\t")
            for row in dictreader:
                self._inventory.append(
                    Inventory(
                        location=row["Location"],
                        name=row["Name"],
                        id=int(row["ID"]),
                        count=int(row["Count"]),
                        slots=int(row["Slots"]),
                    )
                )
