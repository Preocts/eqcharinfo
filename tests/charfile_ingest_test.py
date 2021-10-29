from eqcharinfo.controllers import CharfileIngest

EXPECTED_FILE = "Utske_cazic-Inventory - Copy.txt"

MOCK_WEBFORM = open("tests/fixtures/mock_webform.txt", "r").read().rstrip("\n")
MOCK_CHARFILE = open("tests/fixtures/mock_charfile.txt", "r").read().rstrip("\n")


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
    assert EXPECTED_FILE in result
    assert result[EXPECTED_FILE] == MOCK_CHARFILE


def test_process_webform_error(charfile_ingest: CharfileIngest) -> None:
    result = charfile_ingest.process_webform("Hello")
    assert "error" in result
    assert result["error"] == ""
