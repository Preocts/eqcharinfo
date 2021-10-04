from typing import Generator
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from eqcharinfo import api


@pytest.fixture(scope="function", name="handler")
def fixture_handler() -> Generator[MagicMock, None, None]:
    """Mock all calls, assert calling correct handler"""
    with patch.object(api, "handler") as handler:
        handler.get_all_characters = MagicMock()
        handler.get_inventory = MagicMock()
        handler.character_search = MagicMock()
        yield handler


def test_get_index(handler: MagicMock) -> None:
    """Call correct route"""
    api.get_index()


def test_character_get(handler: MagicMock) -> None:
    """Call correct route"""
    api.get_characters()
    assert handler.get_all_characters.called


def test_show_inventory(handler: MagicMock) -> None:
    """Call correct route"""
    api.show_inventory()
    assert handler.get_inventory.called


def test_character_search(handler: MagicMock) -> None:
    """Call correct route"""
    api.character_search()
    assert handler.character_search.called
