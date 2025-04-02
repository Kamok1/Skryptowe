import subprocess
import os
import argparse
import json
import sys
from collections import Counter

from constans import TOTAL_CHARACTERS, TOTAL_WORDS, TOTAL_LINES, MOST_COMMON_CHAR, MOST_COMMON_WORD, TOTAL_FILES


def analyze_files_in_directory(directory_path):
    files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    results = []

    for file in files:
        file_path = os.path.join(directory_path, file)

        try:
            result = subprocess.run(['python', 'file_analysis.py'], input=file_path, capture_output=True, text=True)
            if result.returncode == 0:
                results.append(json.loads(result.stdout))
            else:
                print(f"Błąd podczas przetwarzania pliku {file}:\n{result.stderr}")

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {file}: {e}")

    return results


def generate_summary(results):
    results = [res for res in results if isinstance(res,dict)]
    total_files = len(results)
    total_characters = sum([res[TOTAL_CHARACTERS] for res in results])
    total_words = sum([res[TOTAL_WORDS] for res in results])
    total_lines = sum([res[TOTAL_LINES] for res in results])

    char_counter = Counter()
    word_counter = Counter()
    for res in results:
        if isinstance(res, dict):
            if res[MOST_COMMON_CHAR]:
                char, count = res[MOST_COMMON_CHAR]
                char_counter[char] += count

            if res[MOST_COMMON_WORD]:
                word, count = res[MOST_COMMON_WORD]
                word_counter[word] += count

    most_common_char = char_counter.most_common(1)
    most_common_word = word_counter.most_common(1)

    return {
        TOTAL_FILES: total_files,
        TOTAL_CHARACTERS: total_characters,
        TOTAL_WORDS: total_words,
        TOTAL_LINES: total_lines,
        MOST_COMMON_CHAR: most_common_char,
        MOST_COMMON_WORD: most_common_word
    }

def parse_args():
    parser = argparse.ArgumentParser(description="Analiza plików w katalogu")
    parser.add_argument("directory", help="Ścieżka do katalogu")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    directory_path = args.directory

    if not os.path.isdir(directory_path):
        print(f"Podana ścieżka {directory_path} nie jest katalogiem.")
        sys.exit(1)

    results = analyze_files_in_directory(directory_path)
    print(json.dumps(generate_summary(results), indent=4))

