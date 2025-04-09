import csv
from datetime import datetime
from pathlib import Path
from utils import get_logger
from consts import *

logger = get_logger("data_loader", False)

def parse_metadata(path):
    logger.info(f"Otwieranie pliku metadanych: {path}")
    try:
        with path.open("r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            headers = [h.strip() for h in next(reader)]
            stations = []

            for row in reader:
                if len(row) == len(headers):
                    stations.append(dict(zip(headers, [cell.strip() for cell in row])))
                else:
                    logger.warning(f"Pominięto wiersz w metadanych: {row}")

            logger.info(f"Zamknięto plik: {path}")
            return {STATIONS: stations}
    except FileNotFoundError:
        logger.error(f"Nie znaleziono pliku: {path}")
        raise


def parse_measurements(path):
    logger.info(f"Otwieranie pliku pomiarowego: {path}")
    results = []
    try:
        with path.open("r", encoding="utf-8") as file:
            total_bytes = 0
            reader = csv.reader(file, delimiter=",")
            next(reader)
            station_codes = next(reader)[1:]
            indicators = next(reader)[1:]
            avg_times = next(reader)[1:]
            units = next(reader)[1:]
            position_codes = next(reader)[1:]

            stations_info = list(zip(station_codes, indicators, avg_times, units, position_codes))

            for row in reader:
                total_bytes += sum(len(cell.encode("utf-8")) for cell in row)
                logger.debug(f"Odczytano {total_bytes} bajtów")

                try:
                    timestamp = datetime.strptime(row[0], "%m/%d/%y %H:%M")
                except ValueError:
                    continue

                for i, val in enumerate(row[1:]):
                    try:
                        value = float(val)
                    except ValueError:
                        value = None

                    station_code, indicator, avg_time, unit, pos_code = stations_info[i]

                    results.append({
                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M"),
                        "station_code": station_code,
                        "indicator": indicator,
                        "avg_time": avg_time,
                        "unit": unit,
                        "position_code": pos_code,
                        "value": value
                    })
        logger.info(f"Zamknięto plik: {path}")
        return results
    except FileNotFoundError:
        logger.error(f"Nie znaleziono pliku: {path}")
        raise
