import datetime

import pytest

from Lista6.models.TimeSeries import TimeSeries
from Lista6.reporters.SimpleReporter import SimpleReporter
from Lista6.validators.OutlierDetector import OutlierDetector
from Lista6.validators.ThresholdDetector import ThresholdDetector
from Lista6.validators.ZeroSpikeDetector import ZeroSpikeDetector


def test_outlier_detector_detects_outlier():
    dates = [datetime.datetime(2024, 1, i+1) for i in range(5)]
    values = [1.0, 1.0, 1.0, 1.0, 100.0]
    ts = TimeSeries("CO", "ST03", "1h", dates, values, "ppm")
    detector = OutlierDetector(k=1.5)
    anomalies = detector.analyze(ts)
    assert len(anomalies) == 1
    assert "Outlier detected" in anomalies[0]


def test_zero_spike_detector_detects_three_consecutive_zeros():
    dates = [datetime.datetime(2024, 1, i+1) for i in range(6)]
    values = [1.0, 0.0, 0.0, 0.0, 2.0, 3.0]
    ts = TimeSeries("O3", "ST04", "1h", dates, values, "ppm")
    detector = ZeroSpikeDetector()
    anomalies = detector.analyze(ts)
    assert len(anomalies) == 1
    assert "Zero spike detected" in anomalies[0]

def test_threshold_detector_detects_exceeding():
    dates = [datetime.datetime(2024, 1, i+1) for i in range(5)]
    values = [0.5, 0.7, 1.5, 2.0, 10.1]
    ts = TimeSeries("PM10", "ST05", "1h", dates, values, "µg/m3")
    detector = ThresholdDetector(threshold=10.0)
    anomalies = detector.analyze(ts)
    assert len(anomalies) == 1
    assert "Threshold exceeded" in anomalies[0]

@pytest.mark.parametrize("validator", [
    OutlierDetector(k=1.5),
    ZeroSpikeDetector(),
    SimpleReporter(),
    ThresholdDetector(threshold=10.0)
])

def test_detect_all_anomalies_polymorphic(validator):
    dates = [datetime.datetime(2024, 1, i+1) for i in range(5)]
    values = [1.0, 0.0, 0.0, 0.0, 100.0]
    ts = TimeSeries("X", "ST", "1h", dates, values, "unit")
    messages = validator.analyze(ts)
    assert isinstance(messages, list)
    for msg in messages:
        assert isinstance(msg, str)
        assert len(msg) > 0
