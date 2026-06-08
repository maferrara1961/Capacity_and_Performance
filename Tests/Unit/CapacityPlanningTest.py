from datetime import UTC, datetime
import unittest

from CapacityEngine.Application.CapacityCalculator import CapacityCalculator
from CapacityEngine.Application.RiskScorer import RiskScorer
from CapacityEngine.Domain.Constants import MetricName
from CapacityEngine.Domain.Entities import CapacityKpi


class CapacityPlanningTest(unittest.TestCase):
    def test_top_consumers_and_sizing(self):
        Now = datetime.now(UTC)
        Kpis = [
            CapacityKpi("K1", "A", MetricName.CPU, Now, Now, Now, 20, 25, 25, 0, 80),
            CapacityKpi("K2", "B", MetricName.CPU, Now, Now, Now, 90, 95, 95, 10, 5),
        ]
        self.assertEqual(CapacityCalculator().TopConsumers(Kpis)[0].ResourceId, "B")
        self.assertEqual(RiskScorer().ClassifySizing(Kpis[0]), "Oversized")
        self.assertEqual(RiskScorer().ClassifySizing(Kpis[1]), "Undersized")


if __name__ == "__main__":
    unittest.main()
