"""Controller for accessing character inventory data"""
import logging
from configparser import ConfigParser

from eqcharinfo.providers import CharacterInventoryProvider

# from eqcharinfo.utils import fuzzy_search


class CharacterClient:
    """Controller for accessing character inventory data"""

    def __init__(self, config: ConfigParser) -> None:
        """Controller for accessing character inventory data"""
        self.log = logging.getLogger(__name__)

        self.character_client = CharacterInventoryProvider(config["CHARACTERS"])

    def init_client(self) -> None:
        """Performs loading and setup"""
        self.log.debug("Loading characters from file...")
        self.character_client.load_all_characters()
        self.log.debug("Complete. Loaded %d characters", len(self.character_client))

    # def search(self, search_string: str, max_results: int = 50) -> List[Inventory]:
    #     """Searches a character's inventory"""
    #     search_items = {inv.name: inv.id for inv in self._inventory.values()}
    #     result = fuzzy_search.search(search_string, search_items, max_results)
    #     found: List[Inventory] = []
    #     for id in result.values():
    #         found.extend([slot for slot in self._inventory.values() if slot.id == id])
    #     return found
