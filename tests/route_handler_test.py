from eqcharinfo import route_handler


def test_get_characters(routes: route_handler.RouteHandler) -> None:
    """Return something"""
    assert routes.get_characters()
