from typing import Generator

import pytest

from eqcharinfo.characterdb import CharacterDB as DB
from eqcharinfo.models.inventory import Inventory

MOCK_CHR = "mockchar"
MOCK_INV = Inventory("location", "name", "1", "count", "slots")
MOCK_LL = "https://mock"
TEST_ROW_COUNT = 10


@pytest.fixture(scope="function", name="empty_client")
def fixture_empty_client() -> Generator[DB, None, None]:
    """Create client"""
    client = DB(":memory:")
    yield client


@pytest.fixture(scope="function", name="client")
def fixture_client(empty_client: DB) -> Generator[DB, None, None]:
    """Fill some rows for testing"""
    for _ in range(TEST_ROW_COUNT):
        empty_client.create(MOCK_CHR, MOCK_INV, MOCK_LL)

    yield empty_client


def test_create(empty_client: DB) -> None:
    """Create rows"""
    for _ in range(TEST_ROW_COUNT):
        empty_client.create(MOCK_CHR, MOCK_INV, MOCK_LL)

    cursor = empty_client.conn.cursor()
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
