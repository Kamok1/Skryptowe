import datetime

import numpy as np
import pytest

from Lista6.models.TimeSeries import TimeSeries


@pytest.fixture
def sample_series() -> TimeSeries:
    dates = [datetime.datetime(2024, 1, i+1) for i in range(5)]
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    return TimeSeries("NO2", "ST01", "1h", dates, values, "µg/m3")

def test_getitem_by_index(sample_series: TimeSeries) -> None:
    assert sample_series[0] == [(datetime.datetime(2024, 1, 1), 1.0)]

def test_getitem_by_slice(sample_series: TimeSeries) -> None:
    assert sample_series[1:3] == [
        (datetime.datetime(2024, 1, 2), 2.0),
        (datetime.datetime(2024, 1, 3), 3.0)
    ]

def test_getitem_by_existing_date(sample_series: TimeSeries) -> None:
    date = datetime.date(2024, 1, 2)
    assert sample_series[date] == [(datetime.datetime(2024, 1, 2), 2.0)]

def test_getitem_by_missing_date_raises(sample_series: TimeSeries) -> None:
    with pytest.raises(KeyError):
        _ = sample_series[datetime.date(2033, 2, 1)]

def test_mean_stddev_full_data(sample_series: TimeSeries) -> None:
    assert sample_series.mean == pytest.approx(3.0)
    assert sample_series.stddev == pytest.approx(1.4142, rel=1e-3)

def test_mean_stddev_with_none():
    dates = [datetime.datetime(2024, 1, i+1) for i in range(5)]
    values = [1.0, None, 3.0, None, 5.0]
    clean_values = [v for v in values if v is not None]
    ts = TimeSeries("SO2", "ST02", "1h", dates, values, "µg/m3")
    assert ts.mean == pytest.approx(np.mean(clean_values))
    assert ts.stddev == pytest.approx(np.std(clean_values))