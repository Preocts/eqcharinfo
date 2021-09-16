"""Use the Levenshtein Distance table as a base for fuzzy searching"""
from typing import Dict
from typing import List
from typing import MutableSet


def search(search_term: str, values: List[str], max_result: int = 10) -> List[str]:
    """Finds the top N matches of search_term in values"""
    if not values or search_term:
        return []

    # scores = {value: 0 for value in values if value}

    return []
    # for value in scores:
    #     if len(value)


def set_by_length(values: List[str]) -> Dict[int, MutableSet[str]]:
    """Create a map of value length paired with sets of values"""
    results: Dict[int, MutableSet[str]] = {}
    for value in values:
        if len(value) in results:
            results[len(value)].add(value)
        else:
            results[len(value)] = {value}
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


def hamming_distance(string01: str, string02: str) -> int:
    """Number of variance in two equal length strings"""
    if len(string01) != len(string02):
        raise ValueError("Expected equal length strings")
    return sum(xi != yi for xi, yi in zip(string01, string02))


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
    itemlist = [item.name for item in client.lucyitems]
    print(f"list time: {(perf_counter_ns() - tic) / 1_000_000}ms")

    tic = perf_counter_ns()
    results = set_by_length(itemlist)
    print(f"set time: {(perf_counter_ns() - tic) / 1_000_000}ms")

    print()
    print(f"Length of list: {len(itemlist)}")
    print(f"Length of results: {len(results)}")

    print("Word Length | Number of words")
    for length in sorted(results.keys()):
        print(f"{length:>10} | {len(results[length]):>5}")
