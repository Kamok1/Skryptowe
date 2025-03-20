import io
from typing import TextIO

from shared import clean_line
from constants import EDITION_MARKER, NEW_LINE_SIGN, NUM_LINES_TO_CHECK

class ContentStream(io.TextIOWrapper):
    def __init__(self, buffer: TextIO):
        self.end_of_stream = False
        super().__init__(buffer.buffer, encoding=buffer.encoding, errors='replace')
        self._init_set_head_position(buffer, EDITION_MARKER, NUM_LINES_TO_CHECK)

    def _init_set_head_position(self, stream: TextIO, edition_marker: str, num_lines_to_check: int) -> bool:
        preamble_detected = False
        consecutive_blank_lines = 0
        line_count = 0
        original_position = stream.tell()
        position_after_preamble = original_position

        while line_count < num_lines_to_check:
            line = stream.readline()

            if not line:
                break

            cleaned = clean_line(line)
            line_count += 1

            if cleaned.startswith(edition_marker):
                stream.seek(original_position)
                return False

            if cleaned == "":
                consecutive_blank_lines += 1
                if consecutive_blank_lines >= 2:
                    preamble_detected = True
                    position_after_preamble = stream.tell()
                    break
            else:
                consecutive_blank_lines = 0

        stream.seek(position_after_preamble if preamble_detected else original_position)
        return preamble_detected


    def _check_end_of_stream(self, line: str) -> bool:
        if line.strip() == EDITION_MARKER:
            self.end_of_stream = True
        return self.end_of_stream

    def read(self, size: int = -1) -> str:
        if self.end_of_stream:
            return ""

        result = ""
        while not self.end_of_stream:
            line = super().readline(size)
            if not line or self._check_end_of_stream(line):
                break
            result += line
        return result

    def readline(self, size: int = -1) -> str:
        if self.end_of_stream:
            return ""
        line = super().readline(size)
        return "" if self._check_end_of_stream(line) else line

def get_book_body_stream(stream: TextIO) -> ContentStream:
    return ContentStream(stream)

