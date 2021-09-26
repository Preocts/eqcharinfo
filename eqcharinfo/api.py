"""API endpoints which create the View"""
from fastapi import FastAPI
from fastapi import Query
from fastapi.responses import HTMLResponse
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape

from eqcharinfo.route_handler import RouteHandler

handler = RouteHandler()
jinenv = Environment(
    loader=FileSystemLoader("html"),
    autoescape=select_autoescape(["html"]),
)
routes = FastAPI()


@routes.get("/characters", response_class=HTMLResponse)
def get_characters() -> str:
    """List loaded characters"""
    template = jinenv.get_template("characterlist.html")
    return template.render(**handler.get_all_characters())


@routes.get("/character_inventory", response_class=HTMLResponse)
def show_inventory(charnames: list[str] = Query([])) -> str:
    """Show inventory of one or more characters"""
    template = jinenv.get_template("character_inventory.html")
    return template.render(characters=handler.get_inventory(charnames))
