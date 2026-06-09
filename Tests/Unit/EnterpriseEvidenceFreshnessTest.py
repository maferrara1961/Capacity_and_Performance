import unittest
from datetime import UTC, datetime, timedelta

from CapacityEngine.Application.EnterpriseEvidenceService import EnterpriseEvidenceService
from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, FreshnessStatus


class EnterpriseEvidenceFreshnessTest(unittest.TestCase):
    def test_clasifica_evidencia_fresca_stale_y_expirada(self):
        Service = EnterpriseEvidenceService()
        Now = datetime.now(UTC)

        self.assertEqual(FreshnessStatus.FRESH, Service.FreshnessStatus(Now - timedelta(hours=2), Now))
        self.assertEqual(FreshnessStatus.STALE, Service.FreshnessStatus(Now - timedelta(days=3), Now))
        self.assertEqual(FreshnessStatus.EXPIRED, Service.FreshnessStatus(Now - timedelta(days=20), Now))

    def test_confianza_no_trata_missing_como_ok(self):
        Service = EnterpriseEvidenceService()

        Result = Service.MonitoringConfidence([EvidenceState.AVAILABLE, EvidenceState.MISSING])

        self.assertLess(Result, 100)


if __name__ == "__main__":
    unittest.main()
