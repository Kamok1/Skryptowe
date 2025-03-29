import sys
from typing import TextIO

from shared import gen_sentences

def get_longest_sentence(stream: TextIO) -> str:
    longest = ""
    for sentence in gen_sentences(stream):
        if len(sentence) > len(longest):
            longest = sentence
    return longest

def main():
    # with open("books/calineczka.txt", "r", encoding="utf-8") as file:
    #     longest = get_longest_sentence(file)
    #     sys.stdout.write(longest)
    longest = get_longest_sentence(sys.stdin)
    sys.stdout.write(longest)

if __name__ == '__main__':
    main()
