import pandas as pd
import re
from pathlib import Path

from consts import *


def clean_polish_chars(text):
    table = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    return text.translate(table)


def extract_dates(df):
    all_dates = set()
    for col in [METADATA_OPEN_DATE, METADATA_CLOSE_DATE]:
        all_dates.update(df[col].dropna().astype(str).str.extractall(r"(\d{4}-\d{2}-\d{2})")[0].dropna())
    return sorted(all_dates)


def extract_coordinates(df):
    coords = pd.concat([df[METADATA_LATITUDE].astype(str), df[METADATA_LONGITUDE].astype(str)])
    return coords.str.extractall(r"(\d{2,3}\.\d{6})")[0].dropna().unique().tolist()


def extract_hyphenated_station_names(df):
    return df[df[METADATA_STATION_NAME].str.contains(r"\w+\s*-\s*\w+", na=False)][METADATA_STATION_NAME].tolist()


def normalize_station_names(df):
    return df[METADATA_STATION_NAME].dropna().apply(
        lambda x: (x, clean_polish_chars(x.replace(" ", "_")))
    ).tolist()


def check_mob_station_type(df):
    mob_rows = df[df[METADATA_STATION_CODE].astype(str).str.contains(r"MOB$", regex=True, na=False)]

    return mob_rows.apply(
        lambda row: (row[METADATA_STATION_CODE], re.fullmatch(r"mobilna", str(row.get(METADATA_STATION_KIND, "")).strip().lower()) is not None),
        axis=1
    ).tolist()



def extract_three_part_locations(df: pd.DataFrame):
    adresy = df[[METADATA_ADDRESS]].dropna().copy()
    adresy["is_three_parts"] = adresy[METADATA_ADDRESS].str.match(r"[^-]+-\s*[^-]+-\s*[^-]+")
    return adresy[adresy["is_three_parts"]][METADATA_ADDRESS].tolist()


def extract_comma_street_locations(df: pd.DataFrame):
    return df[df[METADATA_ADDRESS].str.contains(r"\b(?:ul|al)\..*,", flags=re.IGNORECASE, na=False)][METADATA_ADDRESS].tolist()


def analyze_stations_csv(file_path: Path):
    df = pd.read_csv(file_path)

    return pd.DataFrame({
        "Dates": [extract_dates(df)],
        "Coordinates": [extract_coordinates(df)],
        "Hyphenated station names": [extract_hyphenated_station_names(df)],
        "Normalized station names": [normalize_station_names(df)],
        "MOB station type check": [check_mob_station_type(df)],
        "Three-part locations": [extract_three_part_locations(df)],
        "Street locations with comma": [extract_comma_street_locations(df)]
    })


def main():
    file_path = Path("./data/stacje.csv")

    if not file_path.exists():
        print(f"Plik {file_path} nie istnieje.")
        return

    df = analyze_stations_csv(file_path)


if __name__ == "__main__":
    main()
