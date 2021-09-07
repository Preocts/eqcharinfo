import logging
import os
import pathlib
import tempfile
from typing import Any
from typing import Generator

import pytest

from eqcharinfo import download_itemlist

TEST_URL = "https://github.com/Preocts/eqcharinfo/blob/main/README.md"
MOCK_GZ = pathlib.Path("./tests/fixtures/mock_itemlist.txt.gz")


@pytest.fixture(scope="function", name="mockfile")
def fixture_mockfile() -> Generator[pathlib.Path, None, None]:
    """Create a temp file that cleans iteself up"""
    try:
        file_desc, path = tempfile.mkstemp()
        os.close(file_desc)
        yield pathlib.Path(path)
    finally:
        os.remove(path)


def test_download_file(mockfile: pathlib.Path, caplog: Any) -> None:
    """Grab a test download file"""

    caplog.set_level(logging.INFO)
    os.remove(mockfile)

    download_itemlist.download_itemlist(TEST_URL, mockfile)

    assert "File saved as" in caplog.text

    download_itemlist.download_itemlist(TEST_URL, mockfile)

    assert "Skipping download" in caplog.text


def test_unpack_file() -> None:
    """Unpack the fixture gzip"""

    try:

        download_itemlist.unpack_itemlist(MOCK_GZ)
        assert MOCK_GZ.with_suffix("").exists()

        body = open(MOCK_GZ.with_suffix(""), "r").read()

        assert "This is just a test file" in body

    finally:

        os.remove(MOCK_GZ.with_suffix(""))
