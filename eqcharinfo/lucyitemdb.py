"""
Manage CRUD fucntions for lucy database
"""
from sqlite3 import Connection
from typing import Any
from typing import List
from typing import Optional

from eqcharinfo.models.lucyitem import LucyItem


class LucyItemDB:
    """Manage CRUD functions for lucy database"""

    def __init__(self, database_connection: Connection) -> None:
        self.conn = database_connection

    def create(self, lucy_item: LucyItem) -> None:
        """Create a row"""
        data = [lucy_item.id, lucy_item.name, lucy_item.lucylink]
        sql = "INSERT INTO lucy_table (id, name, lucylink) VALUES (?, ?, ?)"

        self._execute(sql, data)

    def get(self, item_id: str) -> Optional[LucyItem]:
        """Get a row by item_id"""
        data = [item_id]
        sql = "SELECT id, name, lucylink FROM lucy_table WHERE id=?"

        result = self._execute(sql, data)

        return LucyItem(*result[0]) if result else None

    def update(self, lucy_item: LucyItem) -> None:
        """Updates an existing row"""
        data = [lucy_item.name, lucy_item.lucylink, lucy_item.id]
        sql = "UPDATE lucy_table SET name=?, lucylink=? WHERE id=?"

        self._execute(sql, data)

    def delete(self, lucy_item: LucyItem) -> None:
        """Deletes a row from the table"""
        data = [lucy_item.id]
        sql = "DELETE from lucy_table WHERE id=?"

        self._execute(sql, data)

    def _execute(self, sql: str, data: List[Any] = []) -> List[Any]:
        """Internal use only"""
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, data)
            self.conn.commit()
            return cursor.fetchall()

        finally:
            cursor.close()
