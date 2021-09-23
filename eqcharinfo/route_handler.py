"""Passes control to Controllers from api route triggers"""
import datetime
import logging

from eqcharinfo.controllers import CharacterClient
from eqcharinfo.controllers import LucyItemClient
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

    def get_characters(self) -> dict[str, list[str]]:
        """"""
        self.log.debug("GET requests /characters")
        characters = self.characterclient.character_list()
        self.log.debug("Returning %d characters", len(characters))
        return {"characters": characters}
