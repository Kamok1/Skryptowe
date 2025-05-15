from Lista6.models import TimeSeries
from Lista6.validators.SeriesValidator import SeriesValidator


def _generate_anomaly_message(date, value, series) -> str:
    return f"Outlier detected on {date}: {value} | {repr(series)}"


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float = 2):
        self.k = k

    def analyze(self, series: TimeSeries.TimeSeries) -> list[str]:
        mean = series.mean
        stddev = series.stddev
        if mean is None or stddev is None:
            return []

        outliers = []
        for item in series.data:
            if item.value is not None and (item.value > mean + self.k * stddev or item.value < mean - self.k * stddev):
                outliers.append(_generate_anomaly_message(item.date, item.value, series))

        return outliers


