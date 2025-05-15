import re
from pathlib import Path
from typing import Optional

from Lista5.utils import get_logger

logger = get_logger("data_loader")

PATTERN = re.compile(r"(\d{4})_([A-Za-z0-9]+(?:\([A-Za-z0-9]+\))?)_(\w+)\.csv$")

def get_measurement_keys(file) -> Optional[tuple]:
    match = PATTERN.match(file.name)
    if match:
        year, variable, frequency = match.groups()
        key = (year, variable, frequency)
        return key, file
    else:
        logger.debug(f"Pominięto niedopasowany plik: {file.name}")
        return None

def group_measurement_files_by_key(path) -> dict:
    result:dict = {}

    if not path.exists() or not path.is_dir():
        logger.error(f"Podana ścieżka {path} nie istnieje lub nie jest katalogiem.")
        return result

    logger.info(f"Przeszukiwanie plików w katalogu: {path}")

    for file in path.iterdir():
        if file.is_file() and file.suffix == ".csv":
            key_value = get_measurement_keys(file)
            if key_value:
                key, file = key_value
                if key not in result:
                    result[key] = []
                result[key].append(file)
                logger.info(f"Dopasowano plik: {file.name} → {key}")

    if not result:
        logger.warning("Nie znaleziono żadnych pasujących plików.")
    else:
        logger.info(f"Znaleziono {sum(len(v) for v in result.values())} dopasowań w {len(result)} grupach.")

    return result

def main() -> None:
    path = Path("./data/measurements")
    grouped_files = group_measurement_files_by_key(path)

    for key, files in grouped_files.items():
        print(f"{key}:")
        for file in files:
            print(f"  - {file.name}")


if __name__ == "__main__":
    main()
