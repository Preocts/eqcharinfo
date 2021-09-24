from pathlib import Path

import pytest

from eqcharinfo.models.inventoryslot import InventorySlot
from eqcharinfo.providers import CharacterInventoryProvider as CIP

MOCKPATH = "./tests/fixtures"
MOCKCHARFILE = "mockchar-inventory.txt"
MOCKCHAR = "mockchar"


def test_character_file_list(empty_character_provider: CIP) -> None:
    """Load file list"""
    result = empty_character_provider.character_file_list()
    assert len(result)
    assert MOCKCHARFILE in [file.name for file in result]


def test_character_name_from_file_name(empty_character_provider: CIP) -> None:
    """Character name extraction rule"""
    filename = (Path(MOCKPATH) / MOCKCHARFILE).resolve()
    char_name = empty_character_provider.character_name_from_file_name(filename.name)
    assert char_name == MOCKCHAR


def test_load_from_file(empty_character_provider: CIP) -> None:
    filename = Path(MOCKPATH) / MOCKCHARFILE
    assert empty_character_provider.load_from_file(filename)


def test_load_all_characters(empty_character_provider: CIP) -> None:
    """Load files from directory"""
    empty_character_provider.load_all_characters()
    assert empty_character_provider.characters
    assert MOCKCHAR in empty_character_provider.characters
    assert len(empty_character_provider)


def test_empty_without_load(empty_character_provider: CIP) -> None:
    """Provider should not load files without explicit call"""
    assert not empty_character_provider.characters


def test_get_character_slots(filled_character_provider: CIP) -> None:
    """Pull a single character"""
    filled_character_provider.load_all_characters()
    character_slots = filled_character_provider.get_character_slots(MOCKCHAR)
    assert character_slots
    for slot in character_slots:
        assert isinstance(slot, InventorySlot)


def test_get_character_not_found(filled_character_provider: CIP) -> None:
    """Raise when character isn't found"""
    with pytest.raises(ValueError):
        filled_character_provider.get_character_slots("NotThere")


def test_get_characters(filled_character_provider: CIP) -> None:
    """Pull list of loaded characters"""
    filled_character_provider.load_all_characters()
    assert MOCKCHAR in filled_character_provider.characters
