"""Controller for accessing Lucy Item data"""
import logging
from configparser import ConfigParser
from typing import Optional

from eqcharinfo.models.lucyitem import LucyItem
from eqcharinfo.providers import LucyItemFileManager
from eqcharinfo.providers import LucyItemProvider
from eqcharinfo.utils import fuzzy_search


class LucyItemClient:
    """Controller for accessing Lucy Item data"""

    def __init__(self, config: ConfigParser) -> None:
        """Controller for accessing Lucy Item data"""
        self.log = logging.getLogger(__name__)
        self.file_manager = LucyItemFileManager(config["LUCYITEMS"])
        self.lucy_provider = LucyItemProvider(config["LUCYITEMS"])

        self._items_by_id: dict[str, LucyItem] = {}

    def init_client(self) -> None:
        """Performs loading and setup"""
        self.log.debug("Initializing LucyItemClient...")
        self.file_manager.housekeeping()
        self.file_manager.download_itemlist()
        self.lucy_provider.load_from_recent()
        self._load_items_by_id()
        self.log.debug("Completed. %d items loaded", len(self.lucy_provider))

    def _load_items_by_id(self) -> None:
        """Internal setup only"""
        for item in self.lucy_provider:
            self._items_by_id[item.id] = item

    def get_by_id(self, id: str) -> Optional[LucyItem]:
        """Get an item by id, returns None if not found"""
        return self._items_by_id.get(id)

    def search(self, search_term: str, max_results: int = 50) -> list[LucyItem]:
        """Searches the loaded items and returns best match, up to the max results"""
        search_items = {item.name: item.id for item in self.lucy_provider}
        result = fuzzy_search.search(search_term, search_items, max_results)
        return [self._items_by_id[result_id] for result_id in result.values()]
