import logging
import os
import pathlib
import tempfile
from typing import Any
from typing import Generator
from unittest.mock import patch

import pytest

from eqcharinfo import download_itemlist
from eqcharinfo.utils import runtime_loader

TEST_URL = "https://github.com/Preocts/eqcharinfo/blob/main/README.md"
MOCK_GZ = pathlib.Path("./tests/fixtures/mock_itemlist.txt.gz")
MOCK_GZ_BODY = "This is a test file"
CONFIG = runtime_loader.load_config()["DOWNLOAD-ITEMFILE"]


@pytest.fixture(scope="function", name="mockfile")
def fixture_mockfile() -> Generator[pathlib.Path, None, None]:
    """Create a temp file that cleans itself up, yields Path to file"""
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


def test_housekeeping() -> None:
    mock_path = pathlib.Path("./tests/fixtures").resolve()
    fp, path = tempfile.mkstemp(suffix="deleteme.txt.gz", dir=mock_path)
    os.close(fp)

    with patch.object(download_itemlist, "CONFIG", CONFIG) as mockconfig:
        with patch.object(download_itemlist, "DOWNLOAD_PATH", mock_path):
            mockconfig["keep_for_days"] = "0"

            download_itemlist.housekeeping()

    assert not pathlib.Path(path).exists()
