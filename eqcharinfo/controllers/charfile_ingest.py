"""Controller for ingest and parsing of character files"""
import logging
import re
from configparser import ConfigParser


class CharfileIngest:
    HEADER_PATTERN = r"\bLocation\sName\sID\sCount\sSlots\b"
    ROW_PATTERN = r"^.*?\s.*?\s[0-9]*?\s[0-9]*?\s[0-9]*?$"

    def __init__(self, config: ConfigParser) -> None:
        self.log = logging.getLogger(__name__)
        self.config = config
        self._charfile: dict[str, str] = {}

    def process_webform(self, webform_content: str) -> dict[str, str]:
        """Returns filename:content on success, empty dict on failure"""
        filename = self.extract_filename(webform_content)
        context = self.extract_content(webform_content)

        self._charfile = {filename: context} if filename and context else {"error": ""}
        return self._charfile.copy()

    def extract_filename(self, webform_content: str) -> str:
        """Extract filename from webform, returns empty string on failure"""
        result = re.search(r'filename="(.*?)"', webform_content)
        return result.group(1) if result is not None else ""

    def extract_content(self, webform_content: str) -> str:
        """Extract file body from webform, returns empty string on failure"""
        headers = re.findall(self.HEADER_PATTERN, webform_content)
        rows: list[str] = []
        for line in webform_content.split("\n"):
            if re.match(self.ROW_PATTERN, line):
                rows.append(line)
        if not headers or not rows:
            return ""
        rows.insert(0, headers[0])
        return "\n".join(rows)
