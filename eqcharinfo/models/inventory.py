"""Inventory Data"""
import dataclasses


@dataclasses.dataclass
class Inventory:
    location: str
    name: str
    id: str
    count: str
    slots: str

    def __repr__(self) -> str:
        return f"{self.location}\t{self.name}\t{self.id}\t{self.count}\t{self.slots}"
