from typing import Generator

import pytest

from eqcharinfo.character_inventory_client import CharacterInventoryClient
from eqcharinfo.models.inventory import Inventory

MOCKFILE = "./tests/fixtures/inventory.txt"
NAME = "EQCharacterName"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[CharacterInventoryClient, None, None]:

    client = CharacterInventoryClient()

    yield client


@pytest.fixture(scope="function", name="loadedclient")
def fixture_loadedclient() -> Generator[CharacterInventoryClient, None, None]:

    client = CharacterInventoryClient()
    client.load_from_file(MOCKFILE, NAME)

    yield client


def test_load_file(client: CharacterInventoryClient) -> None:
    """Load the file, assert some basic rules"""
    client.load_from_file(MOCKFILE, NAME)

    assert len(client.get_character(NAME))


def test_load_string(client: CharacterInventoryClient) -> None:
    """Load from string"""
    with open(MOCKFILE, "r", encoding="utf-8") as infile:
        fullfile = infile.read()

    client.load_from_string(fullfile, NAME)

    assert len(client._char_inventories)


def test_get_character(loadedclient: CharacterInventoryClient) -> None:
    """Get a character by name"""
    for inventory in loadedclient.get_character(NAME):
        assert isinstance(inventory, Inventory)


def test_get_character_no_match(loadedclient: CharacterInventoryClient) -> None:
    """Get a non-existing character"""
    result = loadedclient.get_character("Not there")
    assert not result


def test_search_character(loadedclient: CharacterInventoryClient) -> None:
    """Search a character's inventory"""
    result = loadedclient.search_character(NAME, "water")
    assert result


def test_search_character_max_results(loadedclient: CharacterInventoryClient) -> None:
    """Search a character's inventory, limit results"""
    result = loadedclient.search_character(NAME, "s", max_results=2)
    assert len(result) == 2


def test_search_character_no_character(loadedclient: CharacterInventoryClient) -> None:
    """Search with a non existing character"""
    result = loadedclient.search_character("Not there", "water")
    assert not result
