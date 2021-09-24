from typing import Generator
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from eqcharinfo import api


@pytest.fixture(scope="function", name="handler")
def fixture_handler() -> Generator[MagicMock, None, None]:
    """Mock all calls, assert calling correct handler"""
    with patch.object(api, "RouteHandler") as mockhandler:
        yield mockhandler


def test_character_get(handler: MagicMock) -> None:
    """Call correct route"""
    handler.get_characters = MagicMock
    api.get_characters()

    assert handler.get_characters.called
