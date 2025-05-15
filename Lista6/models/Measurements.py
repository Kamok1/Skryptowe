import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List
from Lista5.enums.FileInfo import FileInfo
from Lista5.consts import EXTENDED_DATE_FORMAT
from Lista6.models.Measurement import Measurement
from Lista6.models.TimeSeries import TimeSeries
from Lista6.validators.SeriesValidator import SeriesValidator
from Lista5.group_measurement_files_by_key import get_measurement_keys
from Lista5.data_loader import parse_measurements
from Lista6.enums.StationsInfoType import StationInfo

class Measurements:
    def __init__(self, directory: str):
        self.directory = directory
        self.files = self._identify_csv_files()
        self._loaded_data: dict[tuple[str,str,str,str], TimeSeries] = {}

    def _identify_csv_files(self) -> List[str]:
        return [f for f in os.listdir(self.directory) if f.endswith('.csv')]

    def __len__(self) -> int:
        return len(self.files)

    def __contains__(self, parameter_name: str) -> bool:
        return any((keys := get_measurement_keys(Path(file))) is not None
            and parameter_name == keys[0][FileInfo.VARIABLE.value] for file in self.files)

    def get_by_parameter(self, param_name: str) -> List[TimeSeries]:
        self._load_series_by_key(param_name, FileInfo.VARIABLE)
        return self._get_series_by_key(param_name, StationInfo.VARIABLE)

    def get_by_station(self, station_code: str) -> List[TimeSeries]:
        return self._get_series_by_key(station_code, StationInfo.STATION)

    def _load_series_by_key(self, param_value: str, param_type: FileInfo) -> None:
        keys_to_load = [
            file for file in self.files
            if (measurement_key := get_measurement_keys(Path(file))) and measurement_key[0][
                param_type.value] == param_value
        ]
        self._load_multiple_series(keys_to_load)

    def _get_series_by_key(self, param_value: str, param_type: StationInfo) -> List[TimeSeries]:
        keys_to_load = [key for key in self._loaded_data.keys() if key[param_type.value] == param_value]
        return [self._loaded_data[key] for key in keys_to_load]

    def _load_multiple_series(self, files: List[str]) -> None:
        for file in files:
            self._load_series(file)

    def _load_all_series(self) -> List[TimeSeries]:
        if not self._loaded_data:
            self._load_multiple_series(self.files)
        return list(self._loaded_data.values())

    def detect_all_anomalies(self, validators: List[SeriesValidator], preload: bool = False) -> List[str]:
        if preload:
            self._load_all_series()

        anomalies: List[str] = []

        for series in self._loaded_data.values():
            for validator in validators:
                anomalies.extend(validator.analyze(series))

        return anomalies

    def _load_series(self, file: str) -> None:
        grouped: defaultdict[tuple[str,str,str,str], list[Measurement]] = defaultdict(list)

        result = parse_measurements(Path(os.path.join(self.directory, file)))

        for record in result:
            key = (record.indicator, record.station_code, record.avg_time, record.unit)
            grouped[key].append(record)

        for (indicator, station_code, avg_time, unit), records in grouped.items():
            sorted_records = sorted(records, key=lambda r: r.timestamp)
            dates = [datetime.strptime(r.timestamp, EXTENDED_DATE_FORMAT) for r in sorted_records]
            values = [r.value for r in sorted_records]

            key_string = (indicator, station_code, avg_time, unit)
            if key_string in self._loaded_data:
                ts = self._loaded_data[key_string]
                ts.add_values(dates, values)
            else:
                ts = TimeSeries(indicator, station_code, avg_time, dates, values, unit)
                self._loaded_data[key_string] = ts
