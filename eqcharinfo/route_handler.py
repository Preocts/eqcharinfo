"""Passes control to Controllers from api route triggers"""
import datetime
import logging

from eqcharinfo.controllers import CharacterClient
from eqcharinfo.controllers import LucyItemClient
from eqcharinfo.models import InventorySlot
from eqcharinfo.utils.runtime_loader import RuntimeLoader

# Load runtime settings one time
runtime = RuntimeLoader()
runtime.load_config()
runtime.add_logger()


class RouteHandler:
    """Passes control to Controllers from api route triggers"""

    def __init__(self) -> None:
        """Creates controllers and calls their initializers"""
        self.log = logging.getLogger(__name__)
        self.class_loaded_on = datetime.datetime.now()

        self.lucyclient = LucyItemClient(runtime.get_config())
        self.characterclient = CharacterClient(
            config=runtime.get_config(),
            lucy_provider=self.lucyclient.lucy_provider,
        )

        self.lucyclient.init_client()
        self.characterclient.init_client()

    def get_all_characters(self) -> dict[str, list[str]]:
        """Return list of chacarter"""
        self.log.debug("GET requests /characters")
        characters = self.characterclient.character_list()
        self.log.debug("Returning %d characters", len(characters))
        return {"characters": characters}

    def get_inventory(self, charnames: list[str]) -> dict[str, list[InventorySlot]]:
        """Return inventory of character"""
        self.log.debug("GET request: inventory '%s'", charnames)
        charnames = (
            self.get_all_characters()["characters"] if not charnames else charnames
        )

        inventory = {
            char: self.characterclient.get_character_inventory(char)
            for char in charnames
        }

        return inventory
