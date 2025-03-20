import sys
from typing import TextIO

from constants import NEW_LINE_SIGN
from shared import gen_sentences, gen_words

MIN_NUMBER_OF_CONJUNCTIONS: int = 2


def is_conjunction(word: str) -> bool:
    lw = word.lower()
    return lw == "i" or lw == "oraz" or lw == "ale" or lw == "że" or lw == "lub"


def get_sentences_with_conjunctions(stream: TextIO) -> str:
    result = ""
    for sentence in gen_sentences(stream):
        count = 0
        for word in gen_words(sentence):
            if is_conjunction(word):
                count += 1
            if count >= MIN_NUMBER_OF_CONJUNCTIONS:
                result += sentence + NEW_LINE_SIGN
                break
    return result


def main():
    result = get_sentences_with_conjunctions(sys.stdin)
    sys.stdout.write(result)


if __name__ == '__main__':
    main()
