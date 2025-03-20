import sys
from typing import TextIO

from constants import NEW_LINE_SIGN
from shared import gen_sentences
from content_stream import get_book_body_stream

NUMBER_OF_SENTENCES: int = 20

def get_first_20_sentences(stream: TextIO) -> str:
    result = ""
    count = 0
    for sentence in gen_sentences(stream):
        if count < NUMBER_OF_SENTENCES:
            result += sentence + NEW_LINE_SIGN
            count += 1
        else:
            break
    return result

def main():
    with open("books/calineczka.txt", "r", encoding="utf-8") as file:
        result = get_first_20_sentences(get_book_body_stream(file))
    # result = get_first_20_sentences(sys.stdin)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()
