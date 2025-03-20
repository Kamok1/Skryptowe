import sys
from typing import TextIO

from constants import NEW_LINE_SIGN
from shared import gen_sentences, gen_words

MAX_WORDS: int = 4


def get_sentences_at_most_four_words(stream: TextIO) -> str:
    result = ""
    for sentence in gen_sentences(stream):
        count = 0
        for _ in gen_words(sentence):
            count += 1
        if count <= MAX_WORDS:
            result += sentence + NEW_LINE_SIGN
    return result


def main():
    result = get_sentences_at_most_four_words(sys.stdin)
    sys.stdout.write(result)


if __name__ == '__main__':
    main()
