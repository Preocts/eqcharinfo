from typing import Generator

import pytest

from eqcharinfo.controllers import CharacterClient
from eqcharinfo.utils.runtime_loader import load_config

MOCKPATH = "./tests/fixtures"
MOCKNAME = "mockchar"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[CharacterClient, None, None]:
    """Create fixture client"""
    config = load_config()
    config["CHARACTERS"]["file_path"] = MOCKPATH
    client = CharacterClient(config)
    yield client
