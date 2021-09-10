import os
from pathlib import Path


def most_recent(directory: str, glob_pattern: str) -> str:
    """Return most recent file in directory matching glob pattern"""

    path = Path(directory).resolve()
    if not path.is_dir():
        raise ValueError(f"Not a directory: '{directory}'")

    files = [str(file) for file in path.glob(glob_pattern) if file.is_file()]
    return max(files, key=os.path.getctime)
