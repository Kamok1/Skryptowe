import sys
from typing import TextIO
from shared import gen_sentences, gen_words

def is_other_letter(sentence: str) -> bool:
    prev_first = None
    for word in gen_words(sentence):
        if word:
            current_first = word[0].lower()
            if prev_first is not None and current_first == prev_first:
                return False
            prev_first = current_first
    return True

def get_longest_sentence_no_same_letter(stream: TextIO) -> str:
    candidate = ""
    for sentence in gen_sentences(stream):
        if is_other_letter(sentence) and len(sentence) > len(candidate):
            candidate = sentence
    return candidate

def main():
    # with open('books/calineczka.txt', encoding='utf-8') as f:
    #     result = get_longest_sentence_no_same_letter(f)
    #     sys.stdout.write(result)
    result = get_longest_sentence_no_same_letter(sys.stdin)
    sys.stdout.write(result)


if __name__ == '__main__':
    main()
