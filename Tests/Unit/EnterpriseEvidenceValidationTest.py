from datetime import UTC, datetime
import unittest

from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, FreshnessStatus
from CapacityEngine.Domain.EnterpriseEntities import EvidenceRecord
from CapacityEngine.Domain.EnterpriseValidators import ValidateEvidenceRecord
from CapacityEngine.Domain.Exceptions import ValidationError


class EnterpriseEvidenceValidationTest(unittest.TestCase):
    def test_valida_evidencia_con_estado_explicito(self):
        Evidence = EvidenceRecord(
            "E1",
            "Zabbix",
            "Inventory",
            datetime.now(UTC),
            FreshnessStatus.FRESH,
            EvidenceState.AVAILABLE,
            "host.get",
        )
        ValidateEvidenceRecord(Evidence)

    def test_rechaza_evidencia_sin_referencia(self):
        Evidence = EvidenceRecord("E1", "Zabbix", "Inventory", datetime.now(UTC), FreshnessStatus.FRESH, EvidenceState.MISSING, "")
        with self.assertRaises(ValidationError):
            ValidateEvidenceRecord(Evidence)


if __name__ == "__main__":
    unittest.main()
