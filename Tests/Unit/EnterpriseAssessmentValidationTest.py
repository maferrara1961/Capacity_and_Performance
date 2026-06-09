from datetime import UTC, datetime
import unittest

from CapacityEngine.Domain.EnterpriseConstants import (
    EnterpriseRiskSeverity,
    EvidenceState,
    ForecastConfidence,
    RiskCategory,
    ScopeType,
    ScoreClassification,
    ScoreType,
)
from CapacityEngine.Domain.EnterpriseEntities import ForecastResult, Recommendation, RiskAssessment, RiskRegistryEntry, ScoreAssessment
from CapacityEngine.Domain.EnterpriseValidators import (
    ValidateForecastResult,
    ValidateRecommendation,
    ValidateRiskAssessment,
    ValidateRiskRegistryEntry,
    ValidateScoreAssessment,
)
from CapacityEngine.Domain.Exceptions import ValidationError


class EnterpriseAssessmentValidationTest(unittest.TestCase):
    def test_valida_score_riesgo_registro_recomendacion_y_forecast(self):
        Now = datetime.now(UTC)
        ValidateScoreAssessment(ScoreAssessment("SC1", "RUN1", ScoreType.CAPACITY, ScopeType.ENTERPRISE, "enterprise", 70, ScoreClassification.ATTENTION_REQUIRED, EvidenceState.AVAILABLE, Now))
        ValidateRiskAssessment(RiskAssessment("R1", "RUN1", RiskCategory.CAPACITY, EnterpriseRiskSeverity.HIGH, "Capacidad limitada", ScopeType.TECHNOLOGY_COMPONENT, "C1", EvidenceState.AVAILABLE, "P95 alto", Now))
        ValidateRiskRegistryEntry(RiskRegistryEntry("RR1", "R1", RiskCategory.CAPACITY, EnterpriseRiskSeverity.HIGH, "Capacidad limitada", ("C1",), "Aumentar capacidad", "CapacityLab", EvidenceState.AVAILABLE))
        ValidateRecommendation(Recommendation("REC1", "RR1", EnterpriseRiskSeverity.HIGH, "Aumentar capacidad", "P95 alto", "CapacityLab"))
        ValidateForecastResult(ForecastResult("F1", "RUN1", "C1", "CPU", EvidenceState.AVAILABLE, ForecastConfidence.HIGH, Forecast30Days=70))

    def test_rechaza_score_fuera_de_rango(self):
        with self.assertRaises(ValidationError):
            ValidateScoreAssessment(ScoreAssessment("SC1", "RUN1", ScoreType.CAPACITY, ScopeType.ENTERPRISE, "enterprise", 101, ScoreClassification.CRITICAL, EvidenceState.AVAILABLE, datetime.now(UTC)))

    def test_rechaza_healthy_con_evidencia_faltante(self):
        with self.assertRaises(ValidationError):
            ValidateScoreAssessment(ScoreAssessment("SC1", "RUN1", ScoreType.CAPACITY, ScopeType.ENTERPRISE, "enterprise", 80, ScoreClassification.HEALTHY, EvidenceState.MISSING, datetime.now(UTC)))


if __name__ == "__main__":
    unittest.main()
