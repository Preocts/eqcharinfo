"""Provides access to character inventories from files"""
import csv
import logging
from configparser import SectionProxy
from io import StringIO
from pathlib import Path

from eqcharinfo.models.inventoryslot import InventorySlot
from eqcharinfo.utils.fileutil import get_files_by_pattern


class CharacterInventoryProvider:
    """Provides access to character inventories from files"""

    def __init__(self, config_section: SectionProxy) -> None:
        """
        Provides access to character inventories from files

        Args:
            config_section : A SectionProxy containing the following:
                file_path : Location of character inventory files
                glob_pattern : Pattern of file names to load
        """
        self.log = logging.getLogger(__name__)
        self.file_path = config_section["file_path"]
        self.glob_pattern = config_section["glob_pattern"]

        self._characters: dict[str, list[InventorySlot]] = {}

    def __len__(self) -> int:
        """Number of characters loaded"""
        return len(self._characters)

    @property
    def characters(self) -> list[str]:
        """List of loaded characters"""
        return list(self._characters.keys())

    def get_character_slots(self, character_name: str) -> list[InventorySlot]:
        """Return all inventory slots for a given character"""
        if character_name not in self._characters:
            raise ValueError(f"Character not found: {character_name}")
        return list(self._characters[character_name])

    def character_file_list(self) -> list[Path]:
        """Return all character files from config path"""
        return get_files_by_pattern(self.file_path, self.glob_pattern)

    def load_all_characters(self) -> None:
        """Loads all character files found"""
        files = self.character_file_list()
        for file in files:
            character_name = self.character_name_from_file_name(file.name)

            self.log.info("Loading inventory file `%s`", file)
            contents = self.load_from_file(file)

            self.load_character(character_name, contents)

    def load_character(self, character_name: str, contents: str) -> None:
        """Populates inventory of character from a string"""
        filelike = StringIO(contents)
        self.log.info("Loading inventory file from string. Len: %d", len(contents))
        dictreader = csv.DictReader(filelike, delimiter="\t")
        self._characters[character_name] = []
        for row in dictreader:
            self._characters[character_name].append(
                InventorySlot(
                    location=row["Location"],
                    name=row["Name"],
                    id=row["ID"],
                    count=row["Count"],
                    slots=row["Slots"],
                )
            )

    @staticmethod
    def character_name_from_file_name(file_name: str) -> str:
        """Extract character name from file name"""
        return file_name.split("-")[0].strip()

    @staticmethod
    def load_from_file(path: Path) -> str:
        """Load file contents"""
        with path.open(mode="r", encoding="utf-8") as infile:
            return infile.read()
