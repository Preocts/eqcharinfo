"""Controller for accessing character inventory data"""
import logging
from configparser import ConfigParser

from eqcharinfo.models import GeneralSearchResult
from eqcharinfo.models import InventorySlot
from eqcharinfo.models import SpecificSearchResult
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
    ) -> list[GeneralSearchResult]:
        """Searches a specific character, returns best matching items"""
        slots = self.character_client.get_character_slots(character_name)
        search_items = {slot.name: slot.id for slot in slots}
        search = fuzzy_search.search(search_string, search_items, self.max_results)
        return self._render_general_search_results(search)

    def search_all(self, search_string: str) -> list[GeneralSearchResult]:
        """Searches all characters for best match of search_string"""
        search_items: dict[str, str] = {}
        for character in self.character_client.characters:
            slots = self.character_client.get_character_slots(character)
            search_items.update({slot.name: slot.id for slot in slots})
        search = fuzzy_search.search(search_string, search_items, self.max_results)
        return self._render_general_search_results(search)

    def get_slots_character(
        self, character_name: str, item_id: str
    ) -> list[SpecificSearchResult]:
        """List specific item results from specific character"""
        slots = self.character_client.get_character_slots(character_name)
        results = [slot for slot in slots if slot.id == item_id]
        return self._render_specific_search_results(results)

    def get_slots_all(self, item_id: str) -> dict[str, list[SpecificSearchResult]]:
        """By character name: list of item results found in character"""
        result: dict[str, list[SpecificSearchResult]] = {}
        for character in self.character_client.characters:
            result[character] = self.get_slots_character(character, item_id)
        return result

    @staticmethod
    def _render_specific_search_results(
        items: list[InventorySlot],
    ) -> list[SpecificSearchResult]:
        """Internal use: Generate specific search resturn value"""
        results: list[SpecificSearchResult] = []
        for item in items:
            results.append(
                SpecificSearchResult(
                    id=item.id,
                    name=item.name,
                    lucylink="TBD",
                    location=item.location,
                    count=item.count,
                )
            )
        return results

    @staticmethod
    def _render_general_search_results(
        search_results: dict[str, str]
    ) -> list[GeneralSearchResult]:
        """Internal use: Generate general search return value"""
        results: list[GeneralSearchResult] = []
        for result_name, result_id in search_results.items():
            results.append(
                GeneralSearchResult(
                    id=result_id,
                    name=result_name,
                    lucylink="TDB",
                )
            )
        return results
