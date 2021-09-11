from typing import Generator

import pytest

from eqcharinfo.client.inventoryclient import InventoryClient
from eqcharinfo.models.inventory import Inventory

MOCKFILE = "./tests/fixtures/inventory.txt"
NAME = "inventory.txt"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[InventoryClient, None, None]:

    client = InventoryClient(MOCKFILE)

    yield client


def test_character_name(client: InventoryClient) -> None:
    """Names should be explict or implied from filename"""
    assert client.name == NAME

    newclient = InventoryClient("nofile", "rooHappy")

    assert newclient.name == "rooHappy"


def test_load_file(client: InventoryClient) -> None:
    """Load the file, assert some basic rules"""
    client.load_file()

    assert len(client.inventories)
    assert isinstance(client.inventories[-1], Inventory)


def test_iterator(client: InventoryClient) -> None:
    """YAGNI feature of __iter__"""
    client.load_file()
    for inventory in client:
        assert isinstance(inventory, Inventory)
