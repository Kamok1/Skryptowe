from abc import ABC, abstractmethod
from typing import List
from Lista6.models import TimeSeries


class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries.TimeSeries) -> List[str]:
        pass
