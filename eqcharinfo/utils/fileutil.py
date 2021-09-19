import os
from pathlib import Path


def most_recent(directory: str, glob_pattern: str) -> str:
    """Return most recent file in directory matching glob pattern"""

    files = get_files_by_pattern(directory, glob_pattern)
    return max([str(file) for file in files], key=os.path.getctime)


def get_files_by_pattern(directory: str, glob_pattern: str) -> list[Path]:
    """Return list of files matching pattern"""
    path = Path(directory)
    _raise_directory(path)
    return [file for file in path.glob(glob_pattern) if file.is_file()]


def _raise_directory(path: Path) -> None:
    """Raises ValueError if path is not a directory"""
    if not path.is_dir():
        raise ValueError(f"Not a directory: '{path}'")
