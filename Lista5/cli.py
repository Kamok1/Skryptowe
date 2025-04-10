import argparse
import pandas as pd
import random
from pathlib import Path
from datetime import datetime

from utils import get_logger
from data_loader import parse_metadata, parse_measurements
from consts import *
from group_measurement_files_by_key import group_measurement_files_by_key

logger = get_logger("air_quality")

METADATA_PATH = "data/stacje.csv"
MEASUREMENTS_DIRECTORY = "data/measurements"

def parse_args():
    parser = argparse.ArgumentParser(description="CLI do analizy jakości powietrza")
    parser.add_argument("--measure", help="Mierzona wielkość, np. PM10", default="PM10")
    parser.add_argument("--freq", help="Częstotliwość pomiaru, np. 1g, 24g", default="24g")
    parser.add_argument("--from", dest="start_date", help="Data początkowa (rrrr-mm-dd)", default="2023-01-01")
    parser.add_argument("--to", dest="end_date", help="Data końcowa (rrrr-mm-dd)", default="2023-01-31")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("random_station", help="Zwraca losową stację z danymi")

    stats_parser = subparsers.add_parser("stats", help="Pokazuje statystyki dla stacji")
    stats_parser.add_argument("--station", required=True, help="Kod stacji")

    return parser.parse_args()


def find_measurement_files(measure, freq, path):
    logger.info(f"Szukanie plików pomiarowych dla: {measure}, {freq}")
    files_by_key = group_measurement_files_by_key(path)
    matched_files = []

    for (y, m, f), files in files_by_key.items():
        if m.upper() == measure.upper() and f == freq:
            matched_files.extend(files)
    return matched_files


def filter_measurements(measurements, start, end, station_code=None):
    df = pd.DataFrame(measurements)
    df = filter_measurements_by_date(df, start, end)

    if station_code:
        df = df[df[STATION_CODE] == station_code]
    return df


def filter_measurements_by_date(df, start, end):
    df[TIMESTAMP] = pd.to_datetime(df[TIMESTAMP], errors='coerce')
    return df[(df[TIMESTAMP] >= start) & (df[TIMESTAMP] <= end)]


def get_first_station_with_data(measurements, start, end, preferred_code=None):
    df = pd.DataFrame(measurements)
    df = filter_measurements_by_date(df, start, end)

    if preferred_code:
        if not df[df[STATION_CODE] == preferred_code].empty:
            logger.info(f"Użyto preferowanej stacji: {preferred_code}")
            return preferred_code
        else:
            logger.warning(f"Stacja {preferred_code} nie ma danych w tym przedziale czasu.")

    stations = df[STATION_CODE].unique()
    if len(stations) > 0:
        logger.info(f"Zamieniono na stację z danymi: {stations[0]}")
        return stations[0]

    logger.warning("Brak dostępnych stacji z danymi.")
    return None


def random_station(measurements, start, end, metadata):
    df = filter_measurements(measurements, start, end)
    if df.empty:
        logger.warning("Brak danych w podanym przedziale czasowym.")
        return None
    stations = df[STATION_CODE].unique()
    station = random.choice(stations)
    for s in metadata[STATIONS]:
        if s.get(METADATA_STATION_CODE) == station:
            return s.get("Nazwa stacji", ""), s.get("Adres", "")
    return station, ""


def show_stats(measurements, station_code, start, end):
    logger.info(f"Obliczanie statystyk dla: {station_code} w przedziale {start} – {end}")
    real_station_code = get_first_station_with_data(measurements, start, end, station_code)
    if not real_station_code:
        return None

    df = filter_measurements(measurements, start, end, real_station_code)
    values = pd.to_numeric(df[VALUE], errors='coerce').dropna()
    if values.empty:
        logger.warning(f"Stacja {real_station_code} nie posiada wartości liczbowych w tym zakresie.")
        return None

    mean = values.mean()
    std = values.std()
    return real_station_code, mean, std


def main():
    args = parse_args()

    try:
        start = datetime.strptime(args.start_date, "%Y-%m-%d")
        end = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError as e:
        logger.error(f"Niepoprawny format daty: {e}")
        return

    metadata_path = Path(METADATA_PATH)
    measurement_files = find_measurement_files(args.measure, args.freq, Path(MEASUREMENTS_DIRECTORY))

    if not metadata_path.exists():
        logger.error("Brak pliku metadanych.")
        return
    if not measurement_files:
        logger.error("Nie znaleziono plików pomiarowych.")
        return

    metadata = parse_metadata(metadata_path)

    measurements = []
    for path in measurement_files:
        measurements.extend(parse_measurements(path))

    if args.command == "random_station":
        result = random_station(measurements, start, end, metadata)
        if result:
            name, address = result
            print(f"Stacja: {name}\nAdres: {address}")
        else:
            print("Brak stacji z danymi.")
    elif args.command == "stats":
        result = show_stats(measurements, args.station, start, end)
        if result:
            code, mean, std = result
            print(f"Stacja: {code}")
            print(f"Średnia: {mean:.2f}")
            print(f"Odchylenie standardowe: {std:.2f}")
        else:
            print("Brak danych do analizy.")
    else:
        logger.error(f"Nieznana komenda: {args.command}")


if __name__ == "__main__":
    main()
