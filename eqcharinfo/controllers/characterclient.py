"""Controller for accessing character inventory data"""
import logging
from configparser import ConfigParser

from eqcharinfo.models.searchresult import SearchResult
from eqcharinfo.providers import CharacterInventoryProvider
from eqcharinfo.utils import fuzzy_search


class CharacterClient:
    """Controller for accessing character inventory data"""

    # TODO : We should pull LucyItemClient in composition here for URL links
    def __init__(self, config: ConfigParser) -> None:
        """Controller for accessing character inventory data"""
        self.log = logging.getLogger(__name__)

        self.character_client = CharacterInventoryProvider(config["CHARACTERS"])
        self.max_results = config["DEFAULT"].getint("max_search_results", 10)

    def init_client(self) -> None:
        """Performs loading and setup"""
        self.log.debug("Loading characters from file...")
        self.character_client.load_all_characters()
        self.log.debug("Complete. Loaded %d characters", len(self.character_client))

    def character_list(self) -> list[str]:
        """List of loaded characters, can be empty"""
        return self.character_client.characters

    def search_character(
        self,
        character_name: str,
        search_string: str,
    ) -> list[SearchResult]:
        """Searches a specific character, returns best matching items"""
        slots = self.character_client.get_character_slots(character_name)
        search_items = {slot.name: slot.id for slot in slots}
        search = fuzzy_search.search(search_string, search_items, self.max_results)

        results: list[SearchResult] = []
        for result_name, result_id in search.items():
            results.append(
                SearchResult(
                    character=character_name,
                    id=result_id,
                    name=result_name,
                    lucylink="TDB",
                )
            )
        return results

    # def search(self, search_string: str, max_results: int = 50) -> List[Inventory]:
    #     """Searches a character's inventory"""
    #     search_items = {inv.name: inv.id for inv in self._inventory.values()}
    #     result = fuzzy_search.search(search_string, search_items, max_results)
    #     found: List[Inventory] = []
    #     for id in result.values():
    #         found.extend([slot for slot in self._inventory.values() if slot.id == id])
    #     return found
