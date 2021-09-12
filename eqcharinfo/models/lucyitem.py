import dataclasses


@dataclasses.dataclass
class LucyItem:
    """Matches values from Lucy's itemlist"""

    id: str
    name: str
    lucylink: str
