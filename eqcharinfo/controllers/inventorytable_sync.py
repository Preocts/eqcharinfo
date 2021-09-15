"""
Controller for inserting inventories into the database

Existing inventories by charname are replaced completely
"""
import logging
from configparser import ConfigParser
from sqlite3 import Connection

from eqcharinfo.character_inventory_client import CharacterInventoryClient
from eqcharinfo.inventorydb import InventoryDB


class InventoryTableSync:
    """Controller for inserting/updating inventories to database"""

    def __init__(self, config: ConfigParser, database_connection: Connection) -> None:
        """Controller for inventory database"""
        self.config = config
        self.database_connection = database_connection

        self.log = logging.getLogger(__name__)
        self.inventorydb = InventoryDB(database_connection)
        self.inventories = CharacterInventoryClient()

    def process_inventory(self, character_name: str, contents: str) -> None:
        """Processes an inventory file"""
        self.inventories.load_from_string(contents, character_name)

        self.inventorydb.delete_by_charname(character_name)

        self.inventorydb.batch_create(
            character_name, self.inventories.get_character(character_name)
        )
