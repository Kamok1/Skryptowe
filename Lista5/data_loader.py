import csv
from datetime import datetime
from pathlib import Path
from utils import get_logger
from consts import *

logger = get_logger("data_loader")

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
                        TIMESTAMP: timestamp.strftime("%Y-%m-%d %H:%M"),
                        STATION_CODE: station_code,
                        INDICATOR: indicator,
                        AVERAGE_TIME: avg_time,
                        UNIT: unit,
                        POSITION_CODE: pos_code,
                        VALUE: value
                    })
        logger.info(f"Zamknięto plik: {path}")
        return results
    except FileNotFoundError:
        logger.error(f"Nie znaleziono pliku: {path}")
        raise

def combine_and_export(metadata, measurements, output_file):
    stations = {entry[METADATA_STATION_CODE]: entry for entry in metadata[STATIONS]}
    combined_rows = []

    for record in measurements:
        station_data = stations.get(record[STATION_CODE], {})
        combined = {**record, **station_data}
        combined_rows.append(combined)

    if combined_rows:
        fieldnames = combined_rows[0].keys()

        with output_file.open("w", encoding="utf-8", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(combined_rows)

        logger.info(f"Zapisano {len(combined_rows)} rekordów do pliku CSV: {output_file}")
    else:
        logger.warning("Brak danych do zapisania!")

def run(metadata_path, measurement_path, output_csv):
    logger.info("Przetwarzanie danych...")
    metadata = parse_metadata(metadata_path)
    measurements = parse_measurements(measurement_path)
    combine_and_export(metadata, measurements, output_csv)


if __name__ == "__main__":
    metadata_file = Path("./data/stacje.csv")
    measurement_file = Path("./data/measurements/2023_BbF(PM10)_24g.csv")
    output_file = Path("wynik_polaczony.csv")

    run(metadata_file, measurement_file, output_file)