import dataclasses

from eqcharinfo.models.inventory import Inventory


@dataclasses.dataclass
class CharacterInventory(Inventory):
    charname: str
