"""
Used for creation and maintainence of database file.
"""
from sqlite3 import Connection

CHARACTER_TABLE = (
    "CREATE TABLE IF NOT EXISTS character_table ("
    "charname TEXT, "
    "location TEXT, "
    "name TEXT, "
    "id TEXT, "
    "count TEXT, "
    "slots TEXT, "
    "PRIMARY KEY (charname, location));"
)

LUCY_TABLE = (
    "CREATE TABLE IF NOT EXISTS lucy_table ("
    "id TEXT PRIMARY KEY, "
    "name TEXT NOT NULL, "
    "lucylink TEXT NOT NULL);"
)


class DatabaseManager:
    def __init__(self, database_connection: Connection) -> None:
        """Provide database filepath"""
        self.conn = database_connection

    def create_tables(self) -> None:
        """Creates tables, only if needed"""
        cursor = self.conn.cursor()

        try:
            cursor.execute(CHARACTER_TABLE)
            cursor.execute(LUCY_TABLE)
            self.conn.commit()
        finally:
            cursor.close()
