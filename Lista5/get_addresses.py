import csv
import re
from pathlib import Path

from consts import *


def get_addresses(path, city):
    addresses = []

    pattern = re.compile(r"^(.*?)(?:\s+(\d+[A-Za-z]?))?$")

    with path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=",")

        for row in reader:
            if row.get(METADATA_CITY, "").strip().lower() == city.strip().lower():
                woj = row.get(METADATA_VOIVODESHIP, "").strip()
                miasto = row.get(METADATA_CITY, "").strip()
                adres = row.get(METADATA_ADDRESS, "").strip()

                match = pattern.match(adres)
                if match:
                    ulica = match.group(1).strip()
                    numer = match.group(2) if match.group(2) else ""
                    addresses.append((woj, miasto, ulica, numer))

    return addresses


# def main():
#     path = Path("./data/stacje.csv")
#     city = "Jawor"
#     result = get_addresses(path, city)
#
#     print(f"Adresy stacji w miejscowości: {city}")
#     for entry in result:
#         print(entry)
#
#
# if __name__ == "__main__":
#     main()
