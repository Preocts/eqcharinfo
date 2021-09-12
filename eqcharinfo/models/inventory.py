"""Inventory Data"""
import dataclasses


@dataclasses.dataclass
class Inventory:
    location: str
    name: str
    id: str
    count: str
    slots: str
