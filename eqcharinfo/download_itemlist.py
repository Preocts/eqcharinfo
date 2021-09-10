"""
Downloads and maintains existing downloads (cleanup) of Lucy's itemlist
"""
import os
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import requests

from eqcharinfo.utils import runtime_loader

log = runtime_loader.set_logger(__name__)

CONFIG = runtime_loader.load_config()["DOWNLOAD-ITEMFILE"]
DOWNLOAD_PATH = (Path(__file__).parent / CONFIG.get("download_path")).resolve()
DOWNLOAD_URL = CONFIG["url"]
FILE_PATH = (DOWNLOAD_PATH / datetime.now().strftime(CONFIG.get("filename"))).resolve()


def housekeeping() -> None:
    """Housekeeping to ensure directories and paths exist, cleans up extra backups"""

    DOWNLOAD_PATH.mkdir(exist_ok=True)
    expiry = datetime.now() - timedelta(days=CONFIG.getint("keep_for_days"))

    # Old gz file cleanup
    for file in DOWNLOAD_PATH.glob("*txt.gz"):
        created = datetime.fromtimestamp(os.path.getctime(file))
        if expiry > created:
            os.remove(file)


def download_itemlist(url: str, filepath: Path) -> None:
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


def main() -> int:
    """Point of entry"""

    housekeeping()
    download_itemlist(DOWNLOAD_URL, FILE_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
