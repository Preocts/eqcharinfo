from typing import Generator

import pytest

from eqcharinfo.providers import LucyItemProvider
from eqcharinfo.utils.runtime_loader import RuntimeLoader


@pytest.fixture(scope="function", name="empty_lucy_provider")
def fixture_empty_lucy_provider() -> Generator[LucyItemProvider, None, None]:
    """Create an empty LucyItemProvider"""
    config = RuntimeLoader().get_config()
    config["LUCYITEMS"]["glob_pattern"] = "*.gz"
    config["LUCYITEMS"]["file_path"] = "./tests/fixtures"
    yield LucyItemProvider(config["LUCYITEMS"])


@pytest.fixture(scope="session", name="filled_lucy_provider")
def fixture_filled_lucy_provider() -> Generator[LucyItemProvider, None, None]:
    """Create a loaded LucyItemProvider"""
    config = RuntimeLoader().get_config()
    config["LUCYITEMS"]["glob_pattern"] = "*.gz"
    config["LUCYITEMS"]["file_path"] = "./tests/fixtures"
    provider = LucyItemProvider(config["LUCYITEMS"])
    provider.load_from_recent()
    yield provider
