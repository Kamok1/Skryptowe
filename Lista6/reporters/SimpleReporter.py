class SimpleReporter:
    def analyze(self, series) -> list[str]:
        return [f"Info: {series.indicator} at {series.station_code} has mean = {series.mean}"]
