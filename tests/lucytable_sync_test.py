from typing import Generator

import pytest

from eqcharinfo.controllers.database_manager import DatabaseManager
from eqcharinfo.controllers.lucytable_sync import LucyTableSync
from eqcharinfo.utils import runtime_loader


@pytest.fixture(scope="function", name="controller")
def fixture_controller() -> Generator[LucyTableSync, None, None]:
    """Create an instance of the controller with testing config"""
    config = runtime_loader.load_config()
    config["DOWNLOAD-ITEMFILE"]["glob_patter"] = "*.gz"
    config["DOWNLOAD-ITEMFILE"]["glob_patter"] = "./tests/fixtures"
    with runtime_loader.load_database(":memory:") as dbconnection:
        db_setup = DatabaseManager(dbconnection)
        db_setup.create_tables()

        controller = LucyTableSync(config, dbconnection)

        yield controller


def test_full_run(controller: LucyTableSync) -> None:
    """Runs the controller completely"""
    controller.run_sync()
