"""Model of a returned search result"""
from dataclasses import dataclass


@dataclass
class GeneralSearchResult:
    """Empty model of a search result"""

    id: str
    name: str
    lucylink: str
