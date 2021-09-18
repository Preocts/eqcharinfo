from typing import Generator
from unittest.mock import patch

import pytest

from eqcharinfo.lucyitemclient import LucyItemClient
from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.utils.runtime_loader import load_config

FIXTURE_DIR = "./tests/fixtures"
FIXTURE_PATTERN = "*.gz"
FIXTURE_FILE = "./tests/fixtures/itemlist.gz"


@pytest.fixture(scope="session", name="client")
def fixture_client() -> Generator[LucyItemClient, None, None]:
    """Create client fixture with mocked locations"""
    config = load_config()
    client = LucyItemClient(config["DOWNLOAD-ITEMFILE"])

    with patch.object(client, "file_pattern", FIXTURE_PATTERN):
        with patch.object(client, "file_dir", FIXTURE_DIR):
            yield client


@pytest.fixture(scope="session", name="loadedclient")
def fixture_loadedclient(
    client: LucyItemClient,
) -> Generator[LucyItemClient, None, None]:
    """Loaded fixture"""
    client.load_from_file(FIXTURE_FILE)
    yield client


def test_load_from_recent(client: LucyItemClient) -> None:
    """Find and load fixture file"""

    client.load_from_recent()
    assert client.lucyitems


def test_load_from_file(client: LucyItemClient) -> None:
    """Load specific file"""

    client.load_from_file(FIXTURE_FILE)
    assert client.lucyitems


def test_iter(loadedclient: LucyItemClient) -> None:
    """YAGNI feature"""

    for item in loadedclient:
        assert isinstance(item, LucyItem)
        break


def test_get(loadedclient: LucyItemClient) -> None:
    """Single item fetch"""
    result = loadedclient.get_by_id("1001")

    assert result is not None
    assert result.id == "1001"
    assert result.name == "Cloth Cap"
    assert result.lucylink == "https://lucy.allakhazam.com/item.html?id=1001"


def test_search(loadedclient: LucyItemClient) -> None:
    """Search for items"""
    assert loadedclient.search("water")


def test_search_not_found(loadedclient: LucyItemClient) -> None:
    """Search returns nothing"""
    assert not loadedclient.search("")


def test_search_limited_results(loadedclient: LucyItemClient) -> None:
    """Limit results"""
    assert len(loadedclient.search("s", 2)) == 2
