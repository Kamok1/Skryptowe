import re
from typing import Generator, TextIO

from constants import NEW_LINE_SIGN, NEW_STATEMENT_SIGNS

def gen_lines(stream: TextIO) -> Generator[str, None, None]:
    # for line in stream:
    #     yield line
    line = ""
    for text in stream:
        for ch in text:
            if ch == NEW_LINE_SIGN:
                yield line
                line = ""
            else:
                line += ch
    yield line

def clean_line(line: str) -> str:
    return re.sub(' +', ' ', line.strip())

def gen_sentences(stream: TextIO) -> Generator[str, None, None]:
    sentence = ""
    newline_count = 0
    for text in stream:
        if text == "":
            continue
        for ch in text:
            sentence += ch
            if ch == NEW_LINE_SIGN:
                newline_count += 1
            else:
                newline_count = 0
            if ch in NEW_STATEMENT_SIGNS or newline_count >= 2:
                striped = sentence.strip()
                if striped != "":
                    yield striped
                sentence = ""
                newline_count = 0
    striped = sentence.strip()
    if striped != "":
        yield striped

def gen_words(text: str) -> Generator[str, None, None]:
    word = ""
    for text in text:
        for ch in text:
            if ch.isspace():
                if word != "":
                    yield word
                    word = ""
            else:
                word += ch
    if word != "":
        yield word