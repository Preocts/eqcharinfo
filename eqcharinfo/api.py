from fastapi import FastAPI

from eqcharinfo.route_handler import RouteHandler

handler = RouteHandler()
routes = FastAPI()


@routes.get("/characters")
def get_characters() -> dict[str, list[str]]:
    """Testing things out"""
    return handler.get_characters()
