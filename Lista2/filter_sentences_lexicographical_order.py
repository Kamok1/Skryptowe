import sys
from typing import TextIO

from constants import NEW_LINE_SIGN
from shared import gen_sentences, gen_words


def get_lexicographically_ordered_sentences(stream: TextIO) -> str:
    result = ""
    for sentence in gen_sentences(stream):
        prev = None
        words_count = 0
        is_lex_order = True
        for word in gen_words(sentence):
            lower = word.lower()
            if prev is not None and lower < prev:
                is_lex_order = False
                break
            prev = lower
            words_count += 1
        if is_lex_order and words_count > 1 and prev is not None:
            result += sentence + NEW_LINE_SIGN
    return result


def main():
    result = get_lexicographically_ordered_sentences(sys.stdin)
    sys.stdout.write(result)


if __name__ == '__main__':
    main()
