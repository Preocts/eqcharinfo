"""
This test request two, or more, mock character inventories to be present in
the './tests/fixtures' folder. Adjust NUMBER_OF_MOCK_CHAR as needed.
"""
from typing import Generator

import pytest

from eqcharinfo.controllers import CharacterClient
from eqcharinfo.providers import LucyItemProvider
from eqcharinfo.utils.runtime_loader import RuntimeLoader

MOCKPATH = "./tests/fixtures"
MOCKNAME = "mockchar"

NUMBER_OF_MOCK_CHAR = 2

# All mock character inventories have multiple matches for these
SEARCH_TERM = "Round Cut"

# MOCKNAME inventories have this in more than one slot
SEARCH_ID = "37818"
SEARCH_NAME = "Round Cut Peridot"
SEARCH_SLOTS = {
    "Ear-Slot1",
    "Face-Slot3",
    "Ear-Slot1",
    "Neck-Slot1",
    "Fingers-Slot1",
    "Fingers-Slot1",
}


@pytest.fixture(scope="function", name="client")
def fixture_client(
    filled_lucy_provider: LucyItemProvider,
) -> Generator[CharacterClient, None, None]:
    """Create fixture client"""
    config = RuntimeLoader().get_config()
    config["CHARACTERS"]["file_path"] = MOCKPATH
    client = CharacterClient(config, filled_lucy_provider)
    client.init_client()
    yield client


def test_character_list(client: CharacterClient) -> None:
    """Pull list of loaded characters"""
    assert len(client.character_list()) == NUMBER_OF_MOCK_CHAR
    assert MOCKNAME in client.character_list()


def test_search_character(client: CharacterClient) -> None:
    """Returns list of possible items from character"""
    result = client.search_character(MOCKNAME, SEARCH_TERM)
    assert SEARCH_TERM in result[-1].name
    assert all([r.lucylink for r in result])


def test_search_all(client: CharacterClient) -> None:
    """Returns list of possible items from all characters"""
    result = client.search_all(SEARCH_TERM)
    assert SEARCH_TERM in result[-1].name


def test_get_slots_character(client: CharacterClient) -> None:
    """Returns list of slots with given item from character"""
    result = client.get_slots_character(MOCKNAME, SEARCH_ID)
    slots = set([r.location for r in result])
    assert not slots - SEARCH_SLOTS


def test_get_slots_all(client: CharacterClient) -> None:
    """Returns list of slots by character name with given item from all characters"""
    result = client.get_slots_all(SEARCH_ID)
    assert all([character for character in result])
