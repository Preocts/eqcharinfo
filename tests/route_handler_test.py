"""
These tests offers two results depending on how you run them.

Part of the suite, normal unit level test.

Run solo with coverage: spot dead code as this should touch
close to all written code behind it. These are not unit tests
for downstream units, so 100% coverage is unexpected. However,
this module should not leave any unit untouched. If it does
there is a good chance you have found dead-code.

To run dead-code scan:
    >>> make dead-code
"""
from unittest.mock import patch

from eqcharinfo import route_handler

# Provide at least one fixtured character name
MOCK_CHARNAMES = ["mockchar"]

MOCK_WEBFORM = open("tests/fixtures/mock_webform.txt", "r").read().rstrip("\n")


def test_get_all_characters(routes: route_handler.RouteHandler) -> None:
    """Return something"""
    assert routes.get_all_characters()


def test_get_inventory(routes: route_handler.RouteHandler) -> None:
    """Return something"""
    assert not routes.get_inventory([])
    assert routes.get_inventory(MOCK_CHARNAMES)


def test_character_search(routes: route_handler.RouteHandler) -> None:
    """Return something"""
    assert not routes.character_search([], "")
    assert routes.character_search(MOCK_CHARNAMES, "s")


def test_character_upload_empty(routes: route_handler.RouteHandler) -> None:
    """Return empty dict"""
    assert routes.character_upload("") == {}


def test_character_upload(routes: route_handler.RouteHandler) -> None:
    """Return something"""
    with patch.object(routes.charfileingest, "save_to_file"):
        assert routes.character_upload(MOCK_WEBFORM)
