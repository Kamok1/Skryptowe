import sys
from typing import TextIO

from constants import NEW_LINE_SIGN
from shared import gen_sentences

MARKS: str = '!?'

def get_sentences_with_marks(stream: TextIO) -> str:
    result = ""
    for sentence in gen_sentences(stream):
        if sentence.endswith(tuple(MARKS)):
            result += sentence + NEW_LINE_SIGN
    return result

def main():
    result = get_sentences_with_marks(sys.stdin)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()
