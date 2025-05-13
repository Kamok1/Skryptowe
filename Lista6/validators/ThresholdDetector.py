from Lista6.models import TimeSeries
from Lista6.validators.SeriesValidator import SeriesValidator


def _generate_anomaly_message(threshold, date, value, series):
    return (f"Threshold exceeded on {date} : value = {value} exceeds threshold"
            f" {threshold} | {repr(series)}")

class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float = 10):
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        anomalies = []

        for date, value in series.data:
            if value is not None and (value > self.threshold):
                anomalies.append(_generate_anomaly_message(self.threshold, date, value, series))

        return anomalies


