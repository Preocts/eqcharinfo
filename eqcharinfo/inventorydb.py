"""
Manage CRUD functions for character database
"""
from sqlite3 import Connection
from typing import Any
from typing import List

from eqcharinfo.models.characterinventory import CharacterInventory
from eqcharinfo.models.inventory import Inventory


class InventoryDB:
    """Manage CRUD functions for character database"""

    def __init__(self, database_connection: Connection) -> None:
        self.conn = database_connection

    def create(self, charname: str, inventory: Inventory) -> None:
        """Create an inventory row"""
        data = [
            charname,
            inventory.location,
            inventory.name,
            inventory.id,
            inventory.count,
            inventory.slots,
        ]
        sql = (
            "INSERT INTO character_table "
            "(charname, location, name, id, count, slots) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )

        self._execute(sql, data)

    def get_by_char(self, charname: str) -> List[CharacterInventory]:
        """Return character table rows by character name, can be empty"""
        data = [charname]
        sql = (
            "SELECT location, name, id, count, slots, charname "
            "FROM character_table WHERE charname=?"
        )
        results = self._execute(sql, data)

        return [CharacterInventory(*row) for row in results]

    def get_by_itemid(self, itemid: str) -> List[CharacterInventory]:
        """Return character table rows by itemid, can be empty"""
        data = [itemid]
        sql = (
            "SELECT location, name, id, count, slots, charname "
            "FROM character_table WHERE id=?"
        )
        results = self._execute(sql, data)

        return [CharacterInventory(*row) for row in results]

    def _execute(self, sql: str, data: List[Any] = []) -> List[Any]:
        """Internal use only"""
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, data)
            self.conn.commit()
            return cursor.fetchall()

        finally:
            cursor.close()
