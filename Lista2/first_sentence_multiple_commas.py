import sys
from typing import TextIO

from shared import gen_sentences

SEPARATOR: str = ','
NUMBER_OF_SEPARATORS: int = 2

def get_first_sentence_with_multiple_commas(stream: TextIO) -> str:
    for sentence in gen_sentences(stream):
        if sentence.count(SEPARATOR) >= NUMBER_OF_SEPARATORS:
            return sentence
    return ""

def main():
    sentence = get_first_sentence_with_multiple_commas(sys.stdin)
    sys.stdout.write(sentence)

if __name__ == '__main__':
    main()
