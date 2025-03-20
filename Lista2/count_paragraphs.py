import sys
from typing import TextIO

from shared import NEW_LINE_SIGN

NEW_LINE_NUMBER: int = 2

def gen_paragraphs(stream: TextIO):
    paragraph = ""
    newline_count = 0
    for ch in stream:
        paragraph += ch
        if ch == NEW_LINE_SIGN:
            newline_count += 1
        else:
            newline_count = 0
        if newline_count == NEW_LINE_NUMBER:
            yield paragraph[:-2]
            paragraph = ""
            newline_count = 0

    if paragraph.strip():
        yield paragraph

def main():
    count = 0
    for para in gen_paragraphs(sys.stdin):
        if para.strip():
            count += 1
    sys.stdout.write(str(count))

if __name__ == '__main__':
    main()
