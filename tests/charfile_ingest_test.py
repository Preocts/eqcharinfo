from configparser import ConfigParser
from pathlib import Path
from unittest.mock import patch

from eqcharinfo.controllers import charfile_ingest
from eqcharinfo.controllers import CharfileIngest

EXPECTED_FILE = "Utske_cazic-Inventory-Copy.txt"

MOCK_WEBFORM = open("tests/fixtures/mock_webform.txt", "r").read().rstrip("\n")
MOCK_CHARFILE = open("tests/fixtures/mock_charfile.txt", "r").read().rstrip("\n")


def test_filepath_from_config(charfile_ingest: CharfileIngest) -> None:
    expected = Path("./tests/fixtures").absolute()
    assert charfile_ingest.filepath == expected


def test_extract_filename_success(charfile_ingest: CharfileIngest) -> None:
    result = charfile_ingest.extract_filename(MOCK_WEBFORM)
    assert result == EXPECTED_FILE


def test_extract_filename_failure(charfile_ingest: CharfileIngest) -> None:
    result = charfile_ingest.extract_filename("This is a test")
    assert not result


def test_extract_content_success(charfile_ingest: CharfileIngest) -> None:
    result = charfile_ingest.extract_content(MOCK_WEBFORM)
    assert result == MOCK_CHARFILE


def test_extract_content_no_header(charfile_ingest: CharfileIngest) -> None:
    # Remove lines until body starts
    broken = MOCK_WEBFORM.split("\n")[5:]
    result = charfile_ingest.extract_content("\n".join(broken))
    assert not result


def test_extract_content_no_body(charfile_ingest: CharfileIngest) -> None:
    # Use lines including header but not body
    broken = MOCK_WEBFORM.split("\n")[:5]
    result = charfile_ingest.extract_content("\n".join(broken))
    assert not result


def test_process_webform(charfile_ingest: CharfileIngest) -> None:
    result = charfile_ingest.process_webform(MOCK_WEBFORM)
    assert EXPECTED_FILE in result["filename"]
    assert result["content"] == MOCK_CHARFILE


def test_process_webform_error(charfile_ingest: CharfileIngest) -> None:
    result = charfile_ingest.process_webform("Hello")
    assert "error" in result
    assert result["error"] == "Invalid"


def test_save_file_empty_filename(charfile_ingest: CharfileIngest) -> None:
    charfile = {"filename": "", "content": MOCK_CHARFILE}
    with patch.object(charfile_ingest, "_charfile", charfile):
        assert not charfile_ingest.save_to_file()


def test_save_file(empty_filepath: str, charfile_ingest: CharfileIngest) -> None:
    full_filepath = Path(empty_filepath).absolute()
    filepath = full_filepath.parent
    filename = full_filepath.name
    charfile = {"filename": filename, "content": MOCK_CHARFILE}
    with patch.object(charfile_ingest, "_charfile", charfile):
        with patch.object(charfile_ingest, "filepath", filepath):
            assert charfile_ingest.save_to_file()

    with open(empty_filepath, "r") as infile:
        contents = infile.read()

    assert contents == MOCK_CHARFILE


def test_save_file_error(config: ConfigParser, empty_filepath: str) -> None:
    with patch("eqcharinfo.controllers.charfile_ingest.open") as mock_open:
        mock_open.side_effect = PermissionError
        controller = charfile_ingest.CharfileIngest(config)
        charfile = {"filename": empty_filepath, "content": MOCK_CHARFILE}
        with patch.object(controller, "_charfile", charfile):
            assert not controller.save_to_file()
