from typing import Generator
from unittest.mock import patch

import pytest

from eqcharinfo.lucyitemclient import LucyItemClient
from eqcharinfo.models.lucyitem import LucyItem

FIXTURE_DIR = "./tests/fixtures"
FIXTURE_PATTERN = "*.gz"
FIXTURE_FILE = "./tests/fixtures/itemlist.gz"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[LucyItemClient, None, None]:
    """Create client fixture with mocked locations"""
    client = LucyItemClient()

    with patch.object(client, "FILE_PATTERN", FIXTURE_PATTERN):
        with patch.object(client, "FILE_DIR", FIXTURE_DIR):
            yield client


def test_load_from_recent(client: LucyItemClient) -> None:
    """Find and load fixture file"""

    client.load_from_recent()
    assert client.lucyitems


def test_load_from_file(client: LucyItemClient) -> None:
    """Load specific file"""

    client.load_from_file(FIXTURE_FILE)
    assert client.lucyitems


def test_iter(client: LucyItemClient) -> None:
    """YAGNI feature"""

    client.load_from_recent()
    for item in client:
        assert isinstance(item, LucyItem)
