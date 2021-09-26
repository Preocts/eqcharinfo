from eqcharinfo import route_handler


def test_get_all_characters(routes: route_handler.RouteHandler) -> None:
    """Return something"""
    assert routes.get_all_characters()


def test_get_inventory(routes: route_handler.RouteHandler) -> None:
    """Return something"""
    assert routes.get_inventory([])
