from datetime import datetime


class Station:
    def __init__(self, code: str, name: str, start_date: datetime, station_type: str, province: str, city: str, latitude: float, longitude: float):
        self.code = code
        self.name = name
        self.start_date = start_date
        self.station_type = station_type
        self.province = province
        self.city = city
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return f"Station {self.code}: {self.name}, {self.city}, {self.province}"

    def __repr__(self) -> str:
        return f"Station(code={self.code}, name={self.name}, start_date={self.start_date}, " \
               f"station_type={self.station_type}, province={self.province}, city={self.city}, " \
               f"latitude={self.latitude}, longitude={self.longitude})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Station) and self.code == other.code
