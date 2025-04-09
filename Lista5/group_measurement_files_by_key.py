import re
from pathlib import Path
from utils import get_logger

logger = get_logger("data_loader", False)

def group_measurement_files_by_key(path):
    pattern_with_brackets = re.compile(r"(\d{4})_.*\(([A-Z0-9]+)\)_(\w+)\.csv$")
    pattern_without_brackets = re.compile(r"(\d{4})_([A-Z0-9]+)_(\w+)\.csv$")
    result = {}

    if not path.exists() or not path.is_dir():
        logger.error(f"Podana ścieżka {path} nie istnieje lub nie jest katalogiem.")
        return result

    logger.info(f"Przeszukiwanie plików w katalogu: {path}")

    for file in path.iterdir():
        if file.is_file() and file.suffix == ".csv":
            match = pattern_with_brackets.match(file.name)
            if not match:
                match = pattern_without_brackets.match(file.name)

            if match:
                year, variable, frequency = match.groups()
                key = (year, variable, frequency)

                if key not in result:
                    result[key] = []

                result[key].append(file)
                logger.info(f"Dopasowano plik: {file.name} → {key}")
            else:
                logger.debug(f"Pominięto niedopasowany plik: {file.name}")

    if not result:
        logger.warning("Nie znaleziono żadnych pasujących plików.")
    else:
        logger.info(f"Znaleziono {sum(len(v) for v in result.values())} dopasowań w {len(result)} grupach.")

    return result


# def main():
#     path = Path("./data/measurements")
#     grouped_files = group_measurement_files_by_key(path)
#
#     for key, files in grouped_files.items():
#         print(f"{key}:")
#         for file in files:
#             print(f"  - {file.name}")
#
#
# if __name__ == "__main__":
#     main()
