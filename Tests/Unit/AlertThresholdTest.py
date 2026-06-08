import unittest

from CapacityEngine.Domain.Constants import MetricName
from CapacityEngine.Domain.Entities import AlertThreshold
from CapacityEngine.Domain.Exceptions import ValidationError
from CapacityEngine.Domain.Validators import ValidateThreshold


class AlertThresholdTest(unittest.TestCase):
    def test_rejects_invalid_greater_threshold_order(self):
        Threshold = AlertThreshold("T1", "Resource", MetricName.CPU, 90, 75)
        with self.assertRaises(ValidationError):
            ValidateThreshold(Threshold)


if __name__ == "__main__":
    unittest.main()
