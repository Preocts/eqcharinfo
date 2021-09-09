"""Inventory Data"""
import dataclasses


@dataclasses.dataclass
class Inventory:
    location: str
    name: str
    id: int
    count: int
    slots: int

    def __repr__(self) -> str:
        return f"{self.location}\t{self.name}\t{self.id}\t{self.count}\t{self.slots}"
