import gzip
import logging
import pathlib
from datetime import datetime

import requests

DOWNLOAD_LINK = "https://lucy.allakhazam.com/itemlist.txt.gz"
DOWNLOAD_TARGET = pathlib.Path(__file__).parent.parent / "itemlists"
FILE = DOWNLOAD_TARGET / datetime.now().strftime("itemlist-%Y.%m.%d.txt.gz")

log = logging.getLogger(__name__)


def housekeeping() -> None:
    """Housekeeping to ensure directories and paths exist, cleans up extra backups"""
    DOWNLOAD_TARGET.mkdir(exist_ok=True)

    # TODO: Clean up extra backups


def download_itemlist(url: str, filepath: pathlib.Path) -> None:
    """Downloads the Lucy itemlist, saves to given filepath"""

    if filepath.exists():
        log.info("Skipping download, current version exists as '%s'", filepath)
        return

    log.debug("Downloading itemlist from '%s'", url)

    with requests.get(url, stream=True) as request:
        request.raise_for_status()
        with open(filepath, "wb") as fileout:
            for chunk in request.iter_content(chunk_size=8192):
                fileout.write(chunk)

    log.info("File saved as '%s'", filepath)


def unpack_itemlist(filepath: pathlib.Path) -> None:
    """Decompress the gzip of a given itemlist, will be saved in same path"""

    newfile = filepath.with_suffix("")

    log.info("Unpacking `%s` to `%s`", filepath, newfile)

    with gzip.open(filepath, "rb") as infile:
        with open(newfile, "w", encoding="utf-8") as outfile:
            for line in infile:
                outfile.write(line.decode())


def main() -> int:
    """Point of entry"""

    housekeeping()
    download_itemlist(DOWNLOAD_LINK, FILE)
    unpack_itemlist(FILE)

    return 0


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    log.debug("Launched directly, are you testing?")
    raise SystemExit(main())
