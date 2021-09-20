"""Model of a returned search result"""
from dataclasses import dataclass

from eqcharinfo.models.generalsearchresult import GeneralSearchResult


@dataclass
class SpecificSearchResult(GeneralSearchResult):
    """Empty model of a specific search result"""

    location: str
    count: str
