import gzip
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
MOCK_GZ_BODY = "This is a test file"


@pytest.fixture(scope="function", name="mockfile")
def fixture_mockfile() -> Generator[pathlib.Path, None, None]:
    """Create a temp file that cleans itself up, yields Path to file"""
    try:
        file_desc, path = tempfile.mkstemp()
        os.close(file_desc)
        yield pathlib.Path(path)
    finally:
        os.remove(path)


@pytest.fixture(scope="function", name="mockgz")
def fixture_mockgz(mockfile: pathlib.Path) -> Generator[pathlib.Path, None, None]:
    """Creates a temp `*.txt.gz` file, yields Path to file"""
    gzfile = mockfile.name + ".txt.gz"
    gzpath = mockfile.parent / gzfile
    try:
        with gzip.open(gzpath, "wb") as gfileout:
            gfileout.write(MOCK_GZ_BODY.encode())

        yield gzpath

    finally:

        os.remove(gzpath)


def test_download_file(mockfile: pathlib.Path, caplog: Any) -> None:
    """Grab a test download file"""

    caplog.set_level(logging.INFO)
    os.remove(mockfile)

    download_itemlist.download_itemlist(TEST_URL, mockfile)

    assert "File saved as" in caplog.text

    download_itemlist.download_itemlist(TEST_URL, mockfile)

    assert "Skipping download" in caplog.text


def test_unpack_file(mockgz: pathlib.Path) -> None:
    """Unpack the fixture gzip"""

    body = download_itemlist.unpack_itemlist(mockgz)

    assert MOCK_GZ_BODY in body
