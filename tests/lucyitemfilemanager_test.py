import logging
import os
import pathlib
import tempfile
from typing import Any
from typing import Generator

import pytest

from eqcharinfo.providers.lucyitemfilemanager import LucyItemFileManager
from eqcharinfo.utils.runtime_loader import RuntimeLoader

TEST_URL = "https://github.com/Preocts/eqcharinfo/blob/main/README.md"
CONFIG = RuntimeLoader().get_config()["LUCYITEMS"]


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

    provider = LucyItemFileManager(CONFIG)
    provider.url = TEST_URL
    provider.fullfile_path = mockfile

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

    provider = LucyItemFileManager(CONFIG)
    provider.file_path = mock_path
    provider.retain_for_days = 0

    provider.housekeeping()

    assert not pathlib.Path(path).exists()
