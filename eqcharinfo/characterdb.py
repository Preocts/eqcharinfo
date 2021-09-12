"""
Manage CRUD functions for character database
"""
import logging
import sqlite3
from typing import Any
from typing import List

from eqcharinfo.models.chartablerow import CharTableRow
from eqcharinfo.models.inventory import Inventory


class CharacterDB:
    """Manage CRUD functions for character database"""

    log = logging.getLogger(__name__)

    def __init__(self, dbfile: str) -> None:
        self.dbfile = dbfile
        self.conn = sqlite3.connect(database=dbfile)

        self._create_table()

    def _create_table(self) -> None:
        """Creates table, only if needed"""
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS character_table ("
                "uid INTEGER PRIMARY KEY, "
                "charname TEXT, "
                "location TEXT, "
                "name TEXT, "
                "id TEXT, "
                "count TEXT, "
                "slots TEXT, "
                "lucylink TEXT);"
            )
            self.conn.commit()
        finally:
            cursor.close()

    def create(self, charname: str, inventory: Inventory, lucylink: str = "") -> None:
        """Create an inventory row"""
        data = [charname] + inventory.as_list() + [lucylink]
        sql = (
            "INSERT INTO character_table "
            "(charname, location, name, id, count, slots, lucylink) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)"
        )

        self._execute(sql, data)

    def get_by_char(self, charname: str) -> List[CharTableRow]:
        """Return character table rows by character name, can be empty"""
        data = [charname]
        sql = (
            "SELECT charname, location, name, id, count, slots, lucylink "
            "FROM character_table WHERE charname=?"
        )
        return self._execute(sql, data)

    def get_by_itemid(self, itemid: str) -> List[CharTableRow]:
        """Return character table rows by itemid, can be empty"""
        data = [itemid]
        sql = (
            "SELECT charname, location, name, id, count, slots, lucylink "
            "FROM character_table WHERE id=?"
        )
        return self._execute(sql, data)

    def _execute(self, sql: str, data: List[Any] = []) -> List[Any]:
        """Internal use"""
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, data)
            self.conn.commit()
            return cursor.fetchall()

        finally:
            cursor.close()
