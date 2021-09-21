from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.providers.lucyitemprovider import LucyItemProvider

FIXTURE_PATH = "./tests/fixtures"
FIXTURE_PATTERN = "*.gz"
FIXTURE_FILE = "./tests/fixtures/itemlist.gz"


def test_load_from_recent(empty_lucy_provider: LucyItemProvider) -> None:
    """Find and load fixture file"""

    empty_lucy_provider.load_from_recent()
    assert empty_lucy_provider.lucyitems


def test_load_from_file_and_test_len(empty_lucy_provider: LucyItemProvider) -> None:
    """Load specific file and test len()"""

    empty_lucy_provider.load_from_file(FIXTURE_FILE)
    assert len(empty_lucy_provider)


def test_get_list_no_load(filled_lucy_provider: LucyItemProvider) -> None:
    """Auto load the list if the provider is empty"""
    assert filled_lucy_provider.lucyitems


def test_iteration_with_load(filled_lucy_provider: LucyItemProvider) -> None:
    """Pull list with calling load and test __iter__"""
    filled_lucy_provider.load_from_recent()
    for item in filled_lucy_provider:
        assert isinstance(item, LucyItem)
