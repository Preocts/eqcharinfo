"""Controller for accessing character inventory data"""
import logging
from configparser import ConfigParser

from eqcharinfo.models import GeneralSearchResult
from eqcharinfo.models import InventorySlot
from eqcharinfo.models import SpecificSearchResult
from eqcharinfo.providers import CharacterInventoryProvider
from eqcharinfo.providers import LucyItemProvider
from eqcharinfo.utils import fuzzy_search


class CharacterClient:
    """Controller for accessing character inventory data"""

    def __init__(self, config: ConfigParser, lucy_provider: LucyItemProvider) -> None:
        """Controller for accessing character inventory data"""
        self.log = logging.getLogger(__name__)
        self.lucy_provider = lucy_provider

        self.character_provider = CharacterInventoryProvider(config["CHARACTERS"])
        self.max_results = config["DEFAULT"].getint("max_search_results", 10)

    def init_client(self) -> None:
        """Performs loading and setup"""
        self.log.debug("Loading characters from file...")
        self.character_provider.load_all_characters()
        self.log.debug("Complete. Loaded %d characters", len(self.character_provider))

    def character_list(self) -> list[str]:
        """List of loaded characters, can be empty"""
        return self.character_provider.characters

    def get_character_inventory(self, character_name: str) -> list[InventorySlot]:
        """Return a character's inventory"""
        slots = [
            slot
            for slot in self.character_provider.get_character_slots(character_name)
            if slot.name != "Empty"
        ]
        for slot in slots:
            lucyitem = self.lucy_provider.get_by_id(slot.id)
            slot.lucylink = lucyitem.lucylink if lucyitem is not None else ""
        return slots

    def search_character(
        self,
        character_name: str,
        search_string: str,
    ) -> list[GeneralSearchResult]:
        """Searches a specific character, returns best matching items"""
        slots = self.character_provider.get_character_slots(character_name)
        search_items = {slot.name: slot.id for slot in slots}
        search = fuzzy_search.search(search_string, search_items, self.max_results)
        return self._render_general_search_results(search)

    def search_all(self, search_string: str) -> list[GeneralSearchResult]:
        """Searches all characters for best match of search_string"""
        search_items: dict[str, str] = {}
        for character in self.character_provider.characters:
            slots = self.character_provider.get_character_slots(character)
            search_items.update({slot.name: slot.id for slot in slots})
        search = fuzzy_search.search(search_string, search_items, self.max_results)
        return self._render_general_search_results(search)

    def get_slots_character(
        self, character_name: str, item_id: str
    ) -> list[SpecificSearchResult]:
        """List specific item results from specific character"""
        slots = self.character_provider.get_character_slots(character_name)
        results = [slot for slot in slots if slot.id == item_id]
        return self._render_specific_search_results(results)

    def get_slots_all(self, item_id: str) -> dict[str, list[SpecificSearchResult]]:
        """By character name: list of item results found in character"""
        result: dict[str, list[SpecificSearchResult]] = {}
        for character in self.character_provider.characters:
            result[character] = self.get_slots_character(character, item_id)
        return result

    def _render_specific_search_results(
        self,
        items: list[InventorySlot],
    ) -> list[SpecificSearchResult]:
        """Internal use: Generate specific search resturn value"""
        results: list[SpecificSearchResult] = []
        for item in items:
            lucylink = self.lucy_provider.get_by_id(item.id)
            results.append(
                SpecificSearchResult(
                    id=item.id,
                    name=item.name,
                    lucylink=lucylink.lucylink if lucylink else "",
                    location=item.location,
                    count=item.count,
                )
            )
        return results

    def _render_general_search_results(
        self, search_results: dict[str, str]
    ) -> list[GeneralSearchResult]:
        """Internal use: Generate general search return value"""
        results: list[GeneralSearchResult] = []
        for result_name, result_id in search_results.items():
            lucylink = self.lucy_provider.get_by_id(result_id)
            results.append(
                GeneralSearchResult(
                    id=result_id,
                    name=result_name,
                    lucylink=lucylink.lucylink if lucylink else "",
                )
            )
        return results
