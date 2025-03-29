import json
from collections import Counter
import string
import sys

from constans import FILE_PATH, TOTAL_CHARACTERS, TOTAL_WORDS, TOTAL_LINES, MOST_COMMON_WORD, MOST_COMMON_CHAR


def analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        total_characters = len(content)
        words = content.split()
        total_words = len(words)
        lines = content.splitlines()
        total_lines = len(lines)
        all_chars = [char for char in content if char not in string.whitespace]
        most_common_char = Counter(all_chars).most_common(1)
        most_common_word = Counter(words).most_common(1)

        result = {
            FILE_PATH: file_path,
            TOTAL_CHARACTERS: total_characters,
            TOTAL_WORDS: total_words,
            TOTAL_LINES: total_lines,
            MOST_COMMON_CHAR: most_common_char[0] if most_common_char else None,
            MOST_COMMON_WORD: most_common_word[0] if most_common_word else None
        }

        return result

    except Exception as e:
        print(f"Błąd podczas analizy pliku {file_path}: {e}")
        return None

def save_results_to_json(results):
    try:
        print(json.dumps(results))
    except Exception as e:
        print(f"Błąd podczas zapisywania wyników do JSON: {e}")

def main():
    file_path = sys.stdin.readline().strip()

    if not file_path:
        print("Ścieżka do pliku nie została podana.")
        return

    result = analyze_file(file_path)

    if result:
        results = [result]
        save_results_to_json(results)
    else:
        print(f"Błąd podczas analizy pliku {file_path}.")

if __name__ == "__main__":
    main()
