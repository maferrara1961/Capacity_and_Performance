import unittest

from CapacityEngine.Application.EnterpriseScoringService import EnterpriseScoringService
from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, ScoreClassification
from CapacityEngine.Domain.Exceptions import ValidationError


class EnterpriseScoringTest(unittest.TestCase):
    def test_clasifica_score_en_umbrales_requeridos(self):
        Service = EnterpriseScoringService()
        self.assertEqual(Service.Classify(95), ScoreClassification.EXCELLENT)
        self.assertEqual(Service.Classify(80), ScoreClassification.HEALTHY)
        self.assertEqual(Service.Classify(70), ScoreClassification.ATTENTION_REQUIRED)
        self.assertEqual(Service.Classify(50), ScoreClassification.AT_RISK)
        self.assertEqual(Service.Classify(20), ScoreClassification.CRITICAL)

    def test_no_infiere_healthy_desde_evidencia_faltante(self):
        Service = EnterpriseScoringService()
        self.assertEqual(Service.Classify(90, EvidenceState.MISSING), ScoreClassification.ATTENTION_REQUIRED)
        self.assertEqual(Service.EvidenceAdjustedScore(90, EvidenceState.MISSING), 40)

    def test_rechaza_score_fuera_de_rango(self):
        with self.assertRaises(ValidationError):
            EnterpriseScoringService().Classify(101)


if __name__ == "__main__":
    unittest.main()
