"""Inventory Data"""
import dataclasses


@dataclasses.dataclass
class InventorySlot:
    location: str
    name: str
    id: str
    count: str
    slots: str
