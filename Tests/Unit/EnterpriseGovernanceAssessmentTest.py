import unittest
from datetime import UTC, datetime

from CapacityEngine.Application.EnterpriseGovernanceService import EnterpriseGovernanceService
from CapacityEngine.Domain.EnterpriseConstants import EnterpriseRiskSeverity, EvidenceState, FreshnessStatus
from CapacityEngine.Domain.EnterpriseEntities import EvidenceRecord, TechnologyComponent


class EnterpriseGovernanceAssessmentTest(unittest.TestCase):
    def test_confianza_de_monitoreo_penaliza_evidencia_faltante(self):
        Service = EnterpriseGovernanceService()
        Evidence = [
            EvidenceRecord("E1", "Zabbix", "Metric", datetime.now(UTC), FreshnessStatus.FRESH, EvidenceState.AVAILABLE, "ok"),
            EvidenceRecord("E2", "Zabbix", "Metric", datetime.now(UTC), FreshnessStatus.UNKNOWN, EvidenceState.MISSING, "missing"),
        ]

        self.assertLess(Service.MonitoringConfidence(Evidence), 100)

    def test_lifecycle_end_of_life_es_critico(self):
        Service = EnterpriseGovernanceService()
        Component = TechnologyComponent("C1", "SRV-10001", "Server", "D1", LifecycleStatus="EndOfLife")

        self.assertEqual(EnterpriseRiskSeverity.CRITICAL, Service.LifecycleRisk(Component))

    def test_compliance_desconocido_no_es_compliant(self):
        Service = EnterpriseGovernanceService()
        Component = TechnologyComponent("C1", "SRV-10001", "Server", "D1", SupportStatus="Unknown")

        self.assertEqual(EnterpriseRiskSeverity.MEDIUM, Service.ComplianceRisk(Component))


if __name__ == "__main__":
    unittest.main()
