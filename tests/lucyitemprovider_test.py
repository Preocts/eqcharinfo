from typing import Generator
from unittest.mock import patch

import pytest

from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.providers.lucyitemprovider import LucyItemProvider
from eqcharinfo.utils.runtime_loader import load_config

FIXTURE_PATH = "./tests/fixtures"
FIXTURE_PATTERN = "*.gz"
FIXTURE_FILE = "./tests/fixtures/itemlist.gz"


@pytest.fixture(scope="function", name="provider")
def fixture_provider() -> Generator[LucyItemProvider, None, None]:
    """Create provider fixture with mocked locations"""
    config = load_config()
    provider = LucyItemProvider(config["LUCYITEMS"])

    with patch.object(provider, "glob_pattern", FIXTURE_PATTERN):
        with patch.object(provider, "file_path", FIXTURE_PATH):
            yield provider


def test_load_from_recent(provider: LucyItemProvider) -> None:
    """Find and load fixture file"""

    provider.load_from_recent()
    assert provider.lucyitems


def test_load_from_file(provider: LucyItemProvider) -> None:
    """Load specific file"""

    provider.load_from_file(FIXTURE_FILE)
    assert provider.lucyitems


def test_get_list_no_load(provider: LucyItemProvider) -> None:
    """Auto load the list if the provider is empty"""
    assert provider.lucyitems


def test_iteration_with_load(provider: LucyItemProvider) -> None:
    """Pull list with calling load and test __iter__"""
    provider.load_from_recent()
    for item in provider:
        assert isinstance(item, LucyItem)
