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


def test_get_character(client: CharacterInventoryClient) -> None:
    """"""
    client.load_from_file(MOCKFILE, NAME)
    for inventory in client.get_character(NAME):
        assert isinstance(inventory, Inventory)
