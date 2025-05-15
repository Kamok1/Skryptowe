from typing import List

from Lista6.enums.ValidatorType import ValidatorType
from Lista6.models import TimeSeries
from Lista6.validators.SeriesValidator import SeriesValidator


class CompositeValidator(SeriesValidator):
    def __init__(self, validators: List[SeriesValidator], mode: ValidatorType = ValidatorType.AND):
        self.validators = validators
        self.mode = mode

    def analyze(self, series: TimeSeries.TimeSeries) -> List[str]:
        all_messages = []

        for validator in self.validators:
            messages = validator.analyze(series)
            if self.mode == ValidatorType.AND and messages:
                all_messages.extend(messages)
            elif self.mode == ValidatorType.OR and messages:
                return messages

        return all_messages