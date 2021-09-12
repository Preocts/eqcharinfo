from typing import Generator

import pytest

from eqcharinfo.characterdb import CharacterDB as DB
from eqcharinfo.client.database_manager import DatabaseManager
from eqcharinfo.models.inventory import Inventory
from eqcharinfo.utils.runtime_loader import load_database

MOCK_CHR = "mockchar"
MOCK_INV = Inventory("location", "name", "1", "count", "slots")
TEST_ROW_COUNT = 10


@pytest.fixture(scope="function", name="empty_client")
def fixture_empty_client() -> Generator[DB, None, None]:
    """Create client"""
    database_connection = load_database(":memory:")
    builder = DatabaseManager(database_connection)
    builder.create_tables()

    client = DB(database_connection)
    yield client


@pytest.fixture(scope="function", name="client")
def fixture_client(empty_client: DB) -> Generator[DB, None, None]:
    """Fill some rows for testing"""
    for idx in range(TEST_ROW_COUNT):
        MOCK_INV.location = f"slot{idx}"
        empty_client.create(MOCK_CHR, MOCK_INV)

    yield empty_client


def test_create(client: DB) -> None:
    """Create rows"""
    cursor = client.conn.cursor()
    cursor.execute("SELECT * FROM character_table")
    results = cursor.fetchall()
    assert len(results) == TEST_ROW_COUNT


def test_get_by_char(client: DB) -> None:
    """Get by character name"""
    result = client.get_by_char(MOCK_CHR)

    assert len(result) == TEST_ROW_COUNT


def test_get_by_itemid(client: DB) -> None:
    """Get by character name"""
    result = client.get_by_itemid("1")

    assert len(result) == TEST_ROW_COUNT
