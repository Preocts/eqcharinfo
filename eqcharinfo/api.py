"""API endpoints which create the View"""
from fastapi import Body
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


@routes.get("/", response_class=HTMLResponse)
def index() -> str:
    template = jinenv.get_template("index.html")
    return template.render()


@routes.get("/character_list", response_class=HTMLResponse)
def character_list() -> str:
    """List loaded characters"""
    template = jinenv.get_template("character_list.html")
    return template.render(characters=handler.get_all_characters())


@routes.get("/character_inventory", response_class=HTMLResponse)
def character_inventory(charnames: list[str] = Query([])) -> str:
    """Show inventory of one or more characters"""
    template = jinenv.get_template("character_inventory.html")
    return template.render(characters=handler.get_inventory(charnames))


@routes.get("/character_search", response_class=HTMLResponse)
@routes.post("/character_search", response_class=HTMLResponse)
def character_search(charnames: list[str] = Query([]), search_string: str = "") -> str:
    """Search from one or more character inventory(s)"""
    template = jinenv.get_template("character_search.html")
    results = handler.character_search(charnames, search_string)
    return template.render(
        prior_charnames=charnames,
        prior_search=search_string,
        characters=handler.get_all_characters(),
        results=results,
    )


@routes.get("/character_upload", response_class=HTMLResponse)
@routes.post("/character_upload", response_class=HTMLResponse)
def character_upload(char_file: str = Body("")) -> str:
    template = jinenv.get_template("character_upload.html")
    return template.render(data=handler.character_upload(char_file))
