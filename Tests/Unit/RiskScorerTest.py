from datetime import UTC, datetime
import unittest

from CapacityEngine.Application.RiskScorer import RiskScorer
from CapacityEngine.Domain.Constants import MetricName, RiskLevel
from CapacityEngine.Domain.Entities import AlertThreshold, CapacityKpi, RiskAssessment


class RiskScorerTest(unittest.TestCase):
    def setUp(self):
        self.Scorer = RiskScorer()
        self.Threshold = AlertThreshold("T1", "Resource", MetricName.CPU, 75, 90)

    def test_scores_ok_warning_and_critical(self):
        self.assertEqual(self.Scorer.ScoreValue(50, self.Threshold), RiskLevel.OK)
        self.assertEqual(self.Scorer.ScoreValue(80, self.Threshold), RiskLevel.WARNING)
        self.assertEqual(self.Scorer.ScoreValue(95, self.Threshold), RiskLevel.CRITICAL)

    def test_scores_kpi_and_propagates_dependency_risk(self):
        Now = datetime.now(UTC)
        Kpi = CapacityKpi("K1", "R1", MetricName.CPU, Now, Now, Now, 80, 95, 95, 10, -5)
        Risk = self.Scorer.ScoreKpi(Kpi, self.Threshold)
        self.assertEqual(Risk.OverallRisk, RiskLevel.CRITICAL)
        self.assertEqual(self.Scorer.PropagateDependencyRisk([Risk]), RiskLevel.CRITICAL)


if __name__ == "__main__":
    unittest.main()
