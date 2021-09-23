from typing import Generator
from unittest.mock import patch

import pytest

from eqcharinfo.controllers import LucyItemClient
from eqcharinfo.utils.runtime_loader import RuntimeLoader

FIXTURE_DIR = "./tests/fixtures"
FIXTURE_PATTERN = "*.gz"


@pytest.fixture(scope="session", name="client")
def fixture_client() -> Generator[LucyItemClient, None, None]:
    """Create client fixture"""
    config = RuntimeLoader().get_config()
    config["LUCYITEMS"]["glob_pattern"] = FIXTURE_PATTERN
    config["LUCYITEMS"]["file_path"] = FIXTURE_DIR
    client = LucyItemClient(config)

    with patch.object(client, "file_manager"):
        client.init_client()
        yield client


def test_get(client: LucyItemClient) -> None:
    """Single item fetch"""
    result = client.get_by_id("1001")

    assert result is not None
    assert result.id == "1001"
    assert result.name == "Cloth Cap"
    assert result.lucylink == "https://lucy.allakhazam.com/item.html?id=1001"


def test_search(client: LucyItemClient) -> None:
    """Search for items"""
    assert client.search("water")


def test_search_not_found(client: LucyItemClient) -> None:
    """Search returns nothing"""
    assert not client.search("")


def test_search_limited_results(client: LucyItemClient) -> None:
    """Limit results"""
    assert len(client.search("s", 2)) == 2
