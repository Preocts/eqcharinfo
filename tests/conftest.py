from configparser import ConfigParser
from typing import Generator
from unittest.mock import patch

import pytest

from eqcharinfo import route_handler
from eqcharinfo.controllers import CharacterClient
from eqcharinfo.controllers import CharfileIngest
from eqcharinfo.controllers import LucyItemClient
from eqcharinfo.providers import CharacterInventoryProvider
from eqcharinfo.providers import LucyItemProvider
from eqcharinfo.utils.runtime_loader import RuntimeLoader


@pytest.fixture(scope="session", name="config")
def fixture_config() -> Generator[ConfigParser, None, None]:
    """Config file mock"""
    config = RuntimeLoader().get_config()
    config["LUCYITEMS"]["glob_pattern"] = "*.gz"
    config["LUCYITEMS"]["file_path"] = "./tests/fixtures"
    config["CHARACTERS"]["file_path"] = "./tests/fixtures"
    yield config


@pytest.fixture(scope="function", name="empty_lucy_provider")
def fixture_empty_lucy_provider(
    config: ConfigParser,
) -> Generator[LucyItemProvider, None, None]:
    """Create an empty LucyItemProvider"""
    yield LucyItemProvider(config["LUCYITEMS"])


@pytest.fixture(scope="session", name="filled_lucy_provider")
def fixture_filled_lucy_provider(
    config: ConfigParser,
) -> Generator[LucyItemProvider, None, None]:
    """Create a loaded LucyItemProvider"""
    provider = LucyItemProvider(config["LUCYITEMS"])
    provider.load_from_recent()
    yield provider


@pytest.fixture(scope="function", name="empty_character_provider")
def fixture_empty_character_provider(
    config: ConfigParser,
) -> Generator[CharacterInventoryProvider, None, None]:
    """Create an empty CharacterInventoryProvider"""
    yield CharacterInventoryProvider(config["CHARACTERS"])


@pytest.fixture(scope="session", name="filled_character_provider")
def fixture_filled_character_provider(
    config: ConfigParser,
) -> Generator[CharacterInventoryProvider, None, None]:
    """Create a loaded CharacterInventoryProvider"""
    provider = CharacterInventoryProvider(config["CHARACTERS"])
    provider.load_all_characters()
    yield provider


@pytest.fixture(scope="session", name="charfile_ingest")
def fixture_charfile_ingest(
    config: ConfigParser,
) -> Generator[CharfileIngest, None, None]:
    """Creates a fixture for Charfile ingest"""
    controller = CharfileIngest(config)
    yield controller


@pytest.fixture(scope="session", name="routes")
def fixture_routes(
    config: ConfigParser,
    filled_lucy_provider: LucyItemProvider,
    filled_character_provider: CharacterInventoryProvider,
    charfile_ingest: CharfileIngest,
) -> Generator[route_handler.RouteHandler, None, None]:
    """Creates a fixture"""

    lucyclient = LucyItemClient(config)
    lucyclient.lucy_provider = filled_lucy_provider
    characterclient = CharacterClient(config, lucyclient.lucy_provider)
    characterclient.character_provider = filled_character_provider
    charfileingest = CharfileIngest(config)

    # Ensure mocking of all init calls (test these elsewhere)
    # fmt: off
    with patch.object(route_handler, "LucyItemClient"), \
            patch.object(route_handler, "CharacterClient"), \
            patch.object(route_handler, "CharfileIngest"):

        routes = route_handler.RouteHandler()
        # Insert the conftest fixtures here
        routes.lucyclient = lucyclient
        routes.characterclient = characterclient
        routes.charfileingest = charfileingest

        yield routes
    # fmt: on
