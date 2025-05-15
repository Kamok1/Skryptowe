import datetime
from Lista6.models.Station import Station


def test_station_equality() -> None:
    dt = datetime.datetime(2020, 1, 1)
    s1 = Station("001", "Station A", dt, "type1", "province1", "city1", 50.0, 20.0)
    s2 = Station("001", "Station A", dt, "type1", "province1", "city1", 50.0, 20.0)
    s3 = Station("002", "Station B", dt, "type1", "province1", "city1", 50.0, 20.0)

    assert s1 == s2
    assert s1 != s3
