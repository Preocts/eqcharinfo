import dataclasses


@dataclasses.dataclass
class LucyItem:
    """Matches values from Lucy's itemlist"""

    id: int
    name: str
    lucylink: str
