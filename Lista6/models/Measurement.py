class Measurement:
    def __init__(self,timestamp: str, station_code: str, indicator: str, avg_time: str, unit: str, position_code: str, value: float):
        self.timestamp = timestamp
        self.station_code = station_code
        self.indicator = indicator
        self.avg_time = avg_time
        self.unit = unit
        self.position_code = position_code
        self.value = value
