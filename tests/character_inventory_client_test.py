from typing import Generator

import pytest

from eqcharinfo.character_inventory_client import CharacterInventoryClient
from eqcharinfo.models.inventory import Inventory

MOCKFILE = "./tests/fixtures/inventory.txt"
NAME = "EQCharacterName"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[CharacterInventoryClient, None, None]:

    client = CharacterInventoryClient(NAME)

    yield client


@pytest.fixture(scope="function", name="loadedclient")
def fixture_loadedclient() -> Generator[CharacterInventoryClient, None, None]:

    client = CharacterInventoryClient(NAME)
    client.load_from_file(MOCKFILE)

    yield client


def test_check_name(client: CharacterInventoryClient) -> None:
    """What's a name"""
    assert client.character_name == NAME


def test_load_file(client: CharacterInventoryClient) -> None:
    """Load the file, assert some basic rules"""
    client.load_from_file(MOCKFILE)

    assert len(client._inventory)


def test_load_string(client: CharacterInventoryClient) -> None:
    """Load from string"""
    with open(MOCKFILE, "r", encoding="utf-8") as infile:
        fullfile = infile.read()

    client.load_from_string(fullfile)

    assert len(client._inventory)


def test_get_character(loadedclient: CharacterInventoryClient) -> None:
    """Get a character by name"""
    for inventory in loadedclient:
        assert isinstance(inventory, Inventory)


def test_search_character(loadedclient: CharacterInventoryClient) -> None:
    """Search a character's inventory"""
    result = loadedclient.search("water")
    assert result


def test_search_character_max_results(loadedclient: CharacterInventoryClient) -> None:
    """Search a character's inventory, limit results"""
    result = loadedclient.search("s", max_results=2)
    assert len(result) == 2
