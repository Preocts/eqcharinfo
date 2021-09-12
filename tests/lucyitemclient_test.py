from typing import Generator
from unittest.mock import patch

import pytest

from eqcharinfo.lucyitemclient import LucyItemClient
from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.utils.runtime_loader import load_config

FIXTURE_DIR = "./tests/fixtures"
FIXTURE_PATTERN = "*.gz"
FIXTURE_FILE = "./tests/fixtures/itemlist.gz"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[LucyItemClient, None, None]:
    """Create client fixture with mocked locations"""
    config = load_config()
    client = LucyItemClient(config)

    with patch.object(client, "file_pattern", FIXTURE_PATTERN):
        with patch.object(client, "file_dir", FIXTURE_DIR):
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


def test_get(client: LucyItemClient) -> None:
    """Single item fetch"""
    client.load_from_file(FIXTURE_FILE)
    result = client.get_by_id("1001")

    assert result is not None
    assert result.id == "1001"
    assert result.name == "Cloth Cap"
    assert result.lucylink == "https://lucy.allakhazam.com/item.html?id=1001"
