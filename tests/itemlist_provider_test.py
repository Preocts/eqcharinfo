import logging
import os
import pathlib
import tempfile
from typing import Any
from typing import Generator

import pytest

from eqcharinfo.itemlist_provider import ItemListProvider
from eqcharinfo.utils import runtime_loader

TEST_URL = "https://github.com/Preocts/eqcharinfo/blob/main/README.md"
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

    provider = ItemListProvider(CONFIG)
    provider.file_url = TEST_URL
    provider.file_path = mockfile

    caplog.set_level(logging.INFO)
    os.remove(mockfile)

    provider.download_itemlist()

    assert "File saved as" in caplog.text

    provider.download_itemlist()

    assert "skipping download" in caplog.text


def test_housekeeping() -> None:
    """Clean up handling"""
    mock_path = pathlib.Path("./tests/fixtures")
    fp, path = tempfile.mkstemp(suffix="deleteme.txt.gz", dir=mock_path)
    os.close(fp)

    provider = ItemListProvider(CONFIG)
    provider.dir_path = mock_path
    provider.config["keep_for_days"] = "0"

    provider.housekeeping()

    assert not pathlib.Path(path).exists()
