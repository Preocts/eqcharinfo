from pathlib import Path
from typing import Generator

import pytest

from eqcharinfo.models.inventoryslot import InventorySlot
from eqcharinfo.providers import CharacterInventoryProvider as CIP
from eqcharinfo.utils.runtime_loader import load_config

MOCKPATH = "./tests/fixtures"
MOCKCHARFILE = "mockchar-inventory.txt"
MOCKCHAR = "mockchar"


@pytest.fixture(scope="function", name="provider")
def fixture_provider() -> Generator[CIP, None, None]:
    """Create CharacterInventoryProvider fixture"""
    config = load_config()
    provider = CIP(config["CHARACTERS"])
    provider.file_path = MOCKPATH
    yield provider


def test_character_file_list(provider: CIP) -> None:
    """Load file list"""
    result = provider.character_file_list()
    assert len(result)
    assert MOCKCHARFILE in [file.name for file in result]


def test_character_name_from_file_name(provider: CIP) -> None:
    """Character name extraction rule"""
    filename = (Path(MOCKPATH) / MOCKCHARFILE).resolve()
    assert provider.character_name_from_file_name(filename.name) == MOCKCHAR


def test_load_from_file(provider: CIP) -> None:
    filename = Path(MOCKPATH) / MOCKCHARFILE
    assert provider.load_from_file(filename)


def test_load_all_characters(provider: CIP) -> None:
    """Load files from directory"""
    provider.load_all_characters()
    assert provider.characters
    assert MOCKCHAR in provider.characters
    assert len(provider)


def test_empty_without_load(provider: CIP) -> None:
    """Provider should not load files without explicit call"""
    assert not provider.characters


def test_get_character_slots(provider: CIP) -> None:
    """Pull a single character"""
    provider.load_all_characters()
    character_slots = provider.get_character_slots(MOCKCHAR)
    assert character_slots
    for slot in character_slots:
        assert isinstance(slot, InventorySlot)


def test_get_characters(provider: CIP) -> None:
    """Pull list of loaded characters"""
    provider.load_all_characters()
    assert MOCKCHAR in provider.characters
