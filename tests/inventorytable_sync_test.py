"""
Controller test

These tests have little/no asserts. The purpose is end-to-end
run-times with no failures. Other unit-tests should assert
proper function of smaller units
"""
from typing import Generator

import pytest

from eqcharinfo.controllers.database_manager import DatabaseManager
from eqcharinfo.controllers.inventorytable_sync import InventoryTableSync
from eqcharinfo.utils import runtime_loader

MOCK_FILE = "./tests/fixtures/inventory.txt"


@pytest.fixture(scope="function", name="controller")
def fixture_controller() -> Generator[InventoryTableSync, None, None]:
    """Create an instance of the controller with testing config"""
    config = runtime_loader.load_config()
    with runtime_loader.load_database(":memory:") as dbconnection:
        DatabaseManager(dbconnection).create_tables()

        controller = InventoryTableSync(config, dbconnection)

        yield controller


def test_load_file(controller: InventoryTableSync) -> None:
    """Runs the controller from file input"""
    file_content = open(MOCK_FILE, "r", encoding="utf-8").read()

    controller.process_inventory("mockchar", file_content)
