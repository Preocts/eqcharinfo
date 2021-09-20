from typing import Generator

import pytest

from eqcharinfo.controllers import CharacterClient
from eqcharinfo.utils.runtime_loader import load_config

MOCKPATH = "./tests/fixtures"
MOCKNAME = "mockchar"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[CharacterClient, None, None]:
    """Create fixture client"""
    config = load_config()
    config["CHARACTERS"]["file_path"] = MOCKPATH
    client = CharacterClient(config)
    client.init_client()
    yield client


def test_placeholder(client: CharacterClient) -> None:
    """Placeholder for future dev"""
    assert client


def test_character_list(client: CharacterClient) -> None:
    """Pull list of loaded characters"""
    assert len(client.character_list()) == 1
    assert MOCKNAME in client.character_list()


def test_search_character(client: CharacterClient) -> None:
    """Returns list of possible items from character"""
    result = client.search_character(MOCKNAME, "Round Cut")
    assert result
    assert "Round Cut" in result[-1].name


def test_search_all(client: CharacterClient) -> None:
    """Returns list of possible items from all characters"""
    ...


def test_get_slots_character(client: CharacterClient) -> None:
    """Returns list of slots with given item from character"""
    ...


def test_get_slots_all(client: CharacterClient) -> None:
    """Returns list of slots by character name with given item from all characters"""
    ...
