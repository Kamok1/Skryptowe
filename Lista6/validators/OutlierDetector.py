from Lista6.models import TimeSeries
from Lista6.validators.SeriesValidator import SeriesValidator


def _generate_anomaly_message(date, value, series) -> str:
    return f"Outlier detected on {date}: {value} | {repr(series)}"


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float = 2):
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        mean = series.mean
        stddev = series.stddev
        if mean is None or stddev is None:
            return []

        outliers = []
        for date, value in series.data:
            if value is not None and (value > mean + self.k * stddev or value < mean - self.k * stddev):
                outliers.append(_generate_anomaly_message(date, value, series))

        return outliers

