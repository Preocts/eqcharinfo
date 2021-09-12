"""Inventory Data"""
import dataclasses
from typing import List


@dataclasses.dataclass
class Inventory:
    location: str
    name: str
    id: str
    count: str
    slots: str

    def __repr__(self) -> str:
        return f"{self.location}\t{self.name}\t{self.id}\t{self.count}\t{self.slots}"

    def as_list(self) -> List[str]:
        """REPR as list"""
        # Listed seperately to enforce order
        return [self.location, self.name, self.id, self.count, self.slots]
