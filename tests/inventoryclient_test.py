from typing import Generator

import pytest

from eqcharinfo.inventoryclient import InventoryClient
from eqcharinfo.models.inventory import Inventory

MOCKFILE = "./tests/fixtures/inventory.txt"
NAME = "inventory.txt"


@pytest.fixture(scope="function", name="client")
def fixture_client() -> Generator[InventoryClient, None, None]:

    client = InventoryClient("mocktest")

    yield client


def test_load_file(client: InventoryClient) -> None:
    """Load the file, assert some basic rules"""
    client.load_from_file(MOCKFILE)

    assert len(client.inventories)


def test_load_string(client: InventoryClient) -> None:
    """Load from string"""
    with open(MOCKFILE, "r", encoding="utf-8") as infile:
        fullfile = infile.read()

    client.load_from_string(fullfile)

    assert len(client.inventories)


def test_iterator(client: InventoryClient) -> None:
    """YAGNI feature of __iter__"""
    client.load_from_file(MOCKFILE)
    for inventory in client:
        assert isinstance(inventory, Inventory)
