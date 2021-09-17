"""Use the Levenshtein Distance table as a base for fuzzy searching"""
import re
from typing import Dict


def search(
    search_term: str, values: Dict[str, str], max_result: int = 10
) -> Dict[str, str]:
    """
    Finds the top N matches of search_term in values

    'values' should be [{"item name": "item id"}, ...]
    """
    if not values or not search_term:
        return {}
    limited_values = {
        key: value
        for key, value in values.items()
        if re.findall(search_term.strip(), key, flags=re.I)
    }

    scores = {
        value: levenshtein_distance(search_term.lower(), value.lower())
        for value in limited_values.keys()
        if value
    }

    scores = {key: value for key, value in sorted(scores.items(), key=lambda x: x[1])}

    results: Dict[str, str] = {}
    for idx, key in enumerate(scores):
        if idx >= max_result:
            break
        results[key] = values[key]
    return results


def levenshtein_distance(string01: str, string02: str) -> int:
    """Minimum number of substitutions to make the strings identical"""
    len01 = len(string01) + 1
    len02 = len(string02) + 1

    # Zero fill table width of string02 and depth of string01
    # Column 0 and Row 0 will be prefilled values
    table = [[0 for _ in range(len02)] for _ in range(len01)]

    # Fill Row 0
    table[0] = list(range(len02))

    # Fill Column 0
    for idx, row in enumerate(table):
        row[0] = idx

    for idx1 in range(1, len01):
        for idx2 in range(1, len02):
            match = 0 if string01[idx1 - 1] == string02[idx2 - 1] else 1
            offsets = [
                table[idx1][idx2 - 1] + 1,  # Insert Character
                table[idx1 - 1][idx2] + 1,  # Delete Chracter
                table[idx1 - 1][idx2 - 1] + match,  # Character is replaced
            ]
            table[idx1][idx2] = min(offsets)
    return table[-1][-1]


# def hamming_distance(string01: str, string02: str) -> int:
#     """Number of variance in two equal length strings"""
#     if len(string01) != len(string02):
#         raise ValueError("Expected equal length strings")
#     return sum(xi != yi for xi, yi in zip(string01, string02))


# Testing testing testing
if __name__ == "__main__":
    from time import perf_counter_ns
    from eqcharinfo.utils import runtime_loader
    from eqcharinfo.lucyitemclient import LucyItemClient

    config = runtime_loader.load_config()
    client = LucyItemClient(config["DOWNLOAD-ITEMFILE"])
    tic = perf_counter_ns()
    client.load_from_recent()
    print(f"Load time: {(perf_counter_ns() - tic) / 1_000_000}ms")

    tic = perf_counter_ns()
    itemlist = {item.name: item.id for item in client.lucyitems}
    print(f"list time: {(perf_counter_ns() - tic) / 1_000_000}ms")

    print(f"Length of list: {len(itemlist)}")
    print()

    tic = perf_counter_ns()
    search_term = "water f"
    results = search(search_term, itemlist)
    for key, value in results.items():
        print(key, value)
    print(f"Search time: {(perf_counter_ns() - tic) / 1_000_000}ms")
    print()

    tic = perf_counter_ns()
    for item in client.search(search_term, max_results=50):
        print(item)
    print(f"Class Search time: {(perf_counter_ns() - tic) / 1_000_000}ms")
