"""Controller for ingest and parsing of character files"""
import logging
import re
from configparser import ConfigParser
from pathlib import Path


class CharfileIngest:
    HEADER_PATTERN = r"\bLocation\sName\sID\sCount\sSlots\b"
    ROW_PATTERN = r"^.*?\s.*?\s[0-9]*?\s[0-9]*?\s[0-9]*?$"

    def __init__(self, config: ConfigParser) -> None:
        self.log = logging.getLogger(__name__)
        self.config = config
        self.filepath = Path(config["CHARACTERS"]["file_path"]).absolute()
        self._charfile: dict[str, str] = {"filename": "", "content": ""}

    def process_webform(self, webform_content: str) -> dict[str, str]:
        """Returns filename:content on success, empty dict on failure"""
        filename = self.extract_filename(webform_content)
        content = self.extract_content(webform_content)
        charfile = {"filename": filename, "content": content}
        self._charfile = charfile
        return self._charfile.copy() if filename and content else {"error": "Invalid"}

    def extract_filename(self, webform_content: str) -> str:
        """Extract filename from webform, returns empty string on failure"""
        result = re.search(r'filename="(.*?)"', webform_content)
        return self._rpl_spaces(result.group(1)) if result is not None else ""

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

    def save_to_file(self) -> bool:
        """Saves loaded charfile(s) to disk"""
        try:
            with open(self.filepath / self._charfile["filename"], "w") as outfile:
                outfile.write(self._charfile["content"])
        except OSError as err:
            self.log.error("Failed to save '%s' : %s", self._charfile["filename"], err)
            return False
        return True

    @staticmethod
    def _rpl_spaces(string: str) -> str:
        """Replaces spaces with underscores"""
        string = re.sub(r"\s", "_", string.strip())
        return re.sub(r"_-_", "-", string)
