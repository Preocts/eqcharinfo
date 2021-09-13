from typing import Generator

import pytest

from eqcharinfo.controllers.database_manager import DatabaseManager
from eqcharinfo.lucyitemdb import LucyItemDB as DB
from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.utils.runtime_loader import load_database

MOCK_ITEM = LucyItem("id", "rooHappy", "rooHack")
TEST_ROW_COUNT = 10


@pytest.fixture(scope="function", name="empty_client")
def fixture_empty_client() -> Generator[DB, None, None]:
    """Create client"""
    with load_database(":memory:") as database_connection:
        builder = DatabaseManager(database_connection)
        builder.create_tables()

        client = DB(database_connection)
        yield client


@pytest.fixture(scope="function", name="client")
def fixture_client(empty_client: DB) -> Generator[DB, None, None]:
    """Fill some rows for testing"""
    for idx in range(TEST_ROW_COUNT):
        MOCK_ITEM.id = str(idx)
        empty_client.create(MOCK_ITEM)

    yield empty_client


def test_create(client: DB) -> None:
    """Create rows"""
    cursor = client.conn.cursor()
    cursor.execute("SELECT * FROM lucy_table")
    results = cursor.fetchall()
    assert len(results) == TEST_ROW_COUNT


def test_get(client: DB) -> None:
    """Get by item id"""
    result = client.get("8")

    assert result is not None
    assert result.id == "8"
    assert result.name == "rooHappy"
    assert result.lucylink == "rooHack"


def test_update(client: DB) -> None:
    """Update a row"""
    updated = LucyItem("8", "Happy", "Joy")

    client.update(updated)

    result = client.get("8")
    assert result is not None
    assert result.name == "Happy"
    assert result.lucylink == "Joy"


def test_delete(client: DB) -> None:
    """Delete a row"""
    client.delete(LucyItem("8", "", ""))

    result = client.get("8")
    assert result is None
