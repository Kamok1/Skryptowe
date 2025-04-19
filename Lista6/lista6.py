from Lista6.enums.ValidatorType import ValidatorType
from Lista6.models.Measurements import Measurements
from Lista6.reporters.SimpleReporter import SimpleReporter
from Lista6.utilis.CompositeValidator import CompositeValidator
from Lista6.validators.OutlierDetector import OutlierDetector
from Lista6.validators.ThresholdDetector import ThresholdDetector
from Lista6.validators.ZeroSpikeDetector import ZeroSpikeDetector


def main():
    directory = "../Lista5/data/measurements"

    measurements = Measurements(directory)

    print(f"Znaleziono {len(measurements)} plików pomiarowych.")
    tss = measurements.get_by_parameter("Pb(PM10)")


    parameters = set(ts.indicator for ts in tss)
    print("Dostępne parametry:")
    for param in parameters:
        print(f" - {param}: {len(measurements.get_by_parameter(param))} serii")

    composite_validator = CompositeValidator(
        validators=[ZeroSpikeDetector(), OutlierDetector()],
        mode=ValidatorType.OR
    )

    validators = [OutlierDetector(100), ZeroSpikeDetector(), SimpleReporter(), composite_validator, ThresholdDetector(0.03)]
    anomalies = measurements.detect_all_anomalies(validators, preload=False)

    print(f"Wykryto {len(anomalies)} anomalii.")

if __name__ == "__main__":
    main()
