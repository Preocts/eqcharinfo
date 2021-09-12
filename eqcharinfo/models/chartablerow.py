import dataclasses


@dataclasses.dataclass
class CharTableRow:
    charname: str
    location: str
    name: str
    id: str
    count: str
    slots: str
    lucylink: str
