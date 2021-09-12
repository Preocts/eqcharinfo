"""
Controller for downloading and syncing new Lucy item data to the database
"""
from eqcharinfo.itemlist_provider import ItemListProvider
from eqcharinfo.lucyitemclient import LucyItemClient
from eqcharinfo.lucyitemdb import LucyItemDB
from eqcharinfo.utils import runtime_loader


class LucyTableSync:
    """Controller for downloading and syncing new Lucy item data to the database"""

    def __init__(self) -> None:
        self.config = runtime_loader.load_config()
        self.log = runtime_loader.set_logger(__name__)
        self.database = runtime_loader.load_database(self.config["DATABASE"]["file"])
        self.lucydb = LucyItemDB(self.database)
        self.itemprovider = ItemListProvider(self.config["DOWNLOAD-ITEMFILE"])
        self.itemclient = LucyItemClient(self.config["DOWNLOAD-ITEMFILE"])

    def run_sync(self) -> None:
        """Sync table with Lucy item data"""
        self.itemprovider.housekeeping()
        self.itemprovider.download_itemlist()
        self.itemclient.load_from_recent()
        self._sync_table_new()

    def _sync_table_new(self) -> None:
        """Internal only: handles lucy_item table sync for new creates"""
        db_items = set([item.id for item in self.lucydb.get_all()])
        file_items = set([item.id for item in self.itemclient])
        diff = file_items - db_items
        to_create_raw = [self.itemclient.get_by_id(id) for id in diff]
        to_create = [item for item in to_create_raw if item]
        self.log.info("Syncing data with %s lucy items", len(to_create))
        self.lucydb.batch_create(to_create)


if __name__ == "__main__":
    from eqcharinfo.database_manager import DatabaseManager

    provider = LucyTableSync()
    dbm = DatabaseManager(provider.database)
    dbm.create_tables()
    provider.run_sync()
