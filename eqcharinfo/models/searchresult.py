"""Model of a returned search result"""
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Empty model of a search result"""

    character: str
    id: str
    name: str
    lucylink: str
