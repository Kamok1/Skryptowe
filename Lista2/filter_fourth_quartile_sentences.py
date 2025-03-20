import sys
import math
from typing import TextIO
from constants import NEW_LINE_SIGN
from shared import gen_sentences

QUARTILE: float = 0.25

def get_sentences_stats(stream: TextIO) -> (int, int):
    total = 0
    max_length = 0
    for sentence in gen_sentences(stream):
        total += 1
        max_length = max(len(sentence), max_length)
    return total, max_length

def find_threshold(stream: TextIO, total: int, max_length: int) -> int:
    target = math.ceil(QUARTILE * total)
    for candidate in range(1, max_length):
        count = 0
        stream.seek(0)
        for sentence in gen_sentences(stream):
            if len(sentence) >= candidate:
                count += 1
        if count <= target:
            return candidate
    return max_length

def filter_sentences_by_length(stream: TextIO, threshold: int) -> str:
    result = ""
    stream.seek(0)
    count = 0
    for sentence in gen_sentences(stream):
        if len(sentence) >= threshold:
            count += 1
            result += sentence + NEW_LINE_SIGN
    return result

def get_fourth_quartile_sentences(stream: TextIO) -> str:
    total, max_length = get_sentences_stats(stream)
    if total == 0:
        return ""
    threshold = find_threshold(stream, total, max_length)
    return filter_sentences_by_length(stream, threshold)

def main():
    result = get_fourth_quartile_sentences(sys.stdin)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()
