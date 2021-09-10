import os
import tempfile
from pathlib import Path

import pytest

from eqcharinfo.utils import fileutil


def test_most_recent() -> None:
    """Return most recent file created"""
    try:
        fp, filename = tempfile.mkstemp(suffix=".txt.gz")
        filepath = Path(filename).resolve()
        os.close(fp)

        recent = fileutil.most_recent(str(filepath.parent), "*")

        assert str(filepath) == recent

    finally:
        os.remove(filename)


def test_most_recent_raise() -> None:
    """That's no moon"""
    with pytest.raises(ValueError):
        fileutil.most_recent(__file__, "")
