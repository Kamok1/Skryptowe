import datetime
from typing import Optional

from Lista6.models import TimeSeries
from Lista6.validators.SeriesValidator import SeriesValidator


def _generate_anomaly_message(start_date, end_date, count, series):
    return f"Zero spike detected from {start_date} to {end_date}, total zeros: {count} | {repr(series)}"


class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries.TimeSeries) -> list[str]:
        consecutive_zeros: int = 0
        anomalies: list[str] = []
        start_date: Optional[datetime.datetime] = None

        for i, item in enumerate(series.data):
            if item.value is None or item.value == 0:
                if consecutive_zeros == 0:
                    start_date = item.date
                consecutive_zeros += 1
            else:
                if consecutive_zeros >= 3:
                    anomalies.append(_generate_anomaly_message(start_date, item.date, consecutive_zeros, series))
                consecutive_zeros = 0

        if consecutive_zeros >= 3:
            anomalies.append(_generate_anomaly_message(start_date, series.data[-1].date, consecutive_zeros, series))

        return anomalies
