import csv
import re

from utils import get_logger
from consts import *

logger = get_logger(__name__)

def get_addresses(path, city):
    addresses = []

    pattern = re.compile(r"^(.*?)(?:\s+(\d+[A-Za-z]?))?$")
    try:
        with path.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                if row.get(METADATA_CITY, "").strip().lower() == city.strip().lower():
                    voi = row.get(METADATA_VOIVODESHIP, "").strip()
                    city = row.get(METADATA_CITY, "").strip()
                    address = row.get(METADATA_ADDRESS, "").strip()

                    match = pattern.match(address)
                    if match:
                        street = match.group(1).strip()
                        number = match.group(2) if match.group(2) else ""
                        addresses.append((voi, city, street, number))
    except FileNotFoundError:
        logger.error(f"Nie znaleziono pliku: {path}")
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
