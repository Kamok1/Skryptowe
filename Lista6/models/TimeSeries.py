import datetime
from dataclasses import dataclass
from typing import List, Optional

import numpy as np
from collections import namedtuple

from Lista6.consts import DATE_FORMAT

@dataclass
class DateValue:
    date: datetime.datetime
    value: float

class TimeSeries:
    def __init__(self, indicator: str, station_code: str, avg_time: str, dates: List[datetime.datetime], values: List[float], unit: str):
        self.indicator = indicator
        self.station_code = station_code
        self.avg_time = avg_time
        self.data = [
            DateValue(datetime.datetime.strptime(date, DATE_FORMAT) if isinstance(date, str) else date, value)
            for date, value in zip(dates, values)
        ]
        self.unit = unit

    def __getitem__(self, key: object) -> List[tuple]:
        if isinstance(key, slice):
            return [(item.date, item.value) for item in self.data[key]]
        elif isinstance(key, int):
            item = self.data[key]
            return [(item.date, item.value)]
        elif isinstance(key, (datetime.date, datetime.datetime)):
            key_date = key.date() if isinstance(key, datetime.datetime) else key
            indices = [i for i, item in enumerate(self.data) if item.date.date() == key_date]
            if indices:
                return [(self.data[i].date, self.data[i].value) for i in indices]
            else:
                raise KeyError(f"Date {key} not found.")
        else:
            raise TypeError("Invalid key type. Must be datetime, int, or slice.")

    def add_values(self, new_dates, new_values) -> None:
        new_data = [DateValue(datetime.datetime.strptime(date, DATE_FORMAT) if isinstance(date, str) else date, value)
                    for date, value in zip(new_dates, new_values)]
        self.data.extend(new_data)

    @property
    def mean(self) -> Optional[np.floating]:
        clean_values = [item.value for item in self.data if item.value is not None]
        if len(clean_values) > 0:
            return np.mean(clean_values)
        return None

    @property
    def stddev(self) -> Optional[np.floating]:
        clean_values = [item.value for item in self.data if item.value is not None]
        if len(clean_values) > 0:
            return np.std(clean_values)
        return None

    def __repr__(self) -> str:
        return f"TimeSeries(indicator={self.indicator}, station_code={self.station_code}, " \
               f"averaging_time={self.avg_time}, unit={self.unit}, num_values={len(self.data)})"
