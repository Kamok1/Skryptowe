import sys
from typing import TextIO

from shared import gen_sentences, gen_words


def is_proper_name(word: str) -> bool:
    return bool(word) and word[0].isupper()

def count_sentences_with_proper_names(stream: TextIO) -> (int, int):
    total = 0
    proper_count = 0
    for sentence in gen_sentences(stream):
        total += 1
        first = True
        is_proper = False
        for word in gen_words(sentence):
            if first:
                first = False
                continue
            if is_proper_name(word):
                is_proper = True
                break
        if is_proper:
            proper_count += 1
    return total, proper_count

def main():
    # with open("books/opowiesc_wigilijna.txt", "r", encoding="utf-8") as file:
    #     total, proper_count = count_sentences_with_proper_names(file)
    total, proper_count = count_sentences_with_proper_names(sys.stdin)
    percentage = (proper_count / total * 100) if total > 0 else 0
    sys.stdout.write(f"Total sentences: {total}\n")
    sys.stdout.write(f"Sentences with proper names: {proper_count}\n")
    sys.stdout.write(f"Percentage: {percentage:.2f}%\n")

if __name__ == '__main__':
    main()
