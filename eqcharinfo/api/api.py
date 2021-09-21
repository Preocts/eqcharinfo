from fastapi import FastAPI

from eqcharinfo.controllers import CharacterClient
from eqcharinfo.controllers import LucyItemClient
from eqcharinfo.utils import runtime_loader

runtime_loader.add_logger()

lucyclient = LucyItemClient(runtime_loader.load_config())
characterclient = CharacterClient(
    config=runtime_loader.load_config(),
    lucy_provider=lucyclient.lucy_provider,
)

init_run = False
routes = FastAPI()


@routes.get("/characters")
def get_characters() -> dict[str, list[str]]:
    """Testing things out"""
    if not init_run:
        run_full_init()
    characters = characterclient.character_list()
    return {"characters": characters}


def run_full_init() -> None:
    """Sets API up"""
    lucyclient.init_client()
    characterclient.init_client()

    global init_run
    init_run = True
