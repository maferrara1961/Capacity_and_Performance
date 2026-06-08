from datetime import UTC, datetime
import unittest

from CapacityEngine.Domain.Constants import MetricName
from CapacityEngine.Domain.Entities import MetricSample
from CapacityEngine.Domain.Exceptions import ValidationError
from CapacityEngine.Domain.Validators import RejectDuplicateSamples, ValidateMetricSample


class MetricSampleValidationTest(unittest.TestCase):
    def test_rejects_negative_metric_sample(self):
        Sample = MetricSample("S1", "R1", MetricName.CPU, datetime.now(UTC), -1, "Percent", "Test")
        with self.assertRaises(ValidationError):
            ValidateMetricSample(Sample)

    def test_rejects_duplicate_metric_samples(self):
        Now = datetime.now(UTC)
        First = MetricSample("S1", "R1", MetricName.CPU, Now, 1, "Percent", "Test")
        Second = MetricSample("S2", "R1", MetricName.CPU, Now, 2, "Percent", "Test")
        with self.assertRaises(ValidationError):
            RejectDuplicateSamples([First, Second])


if __name__ == "__main__":
    unittest.main()
