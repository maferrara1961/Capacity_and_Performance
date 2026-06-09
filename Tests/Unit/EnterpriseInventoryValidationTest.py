from datetime import UTC, datetime
import unittest

from CapacityEngine.Domain.EnterpriseConstants import EnterpriseRiskSeverity, EvidenceState, TechnologyDomainName
from CapacityEngine.Domain.EnterpriseEntities import BusinessService, ServiceComponentMap, TechnologyComponent, TechnologyDomain
from CapacityEngine.Domain.EnterpriseValidators import (
    ValidateBusinessService,
    ValidateServiceComponentMap,
    ValidateTechnologyComponent,
    ValidateTechnologyDomain,
)
from CapacityEngine.Domain.Exceptions import ValidationError


class EnterpriseInventoryValidationTest(unittest.TestCase):
    def test_valida_dominio_componente_servicio_y_mapeo(self):
        ValidateTechnologyDomain(TechnologyDomain("D1", TechnologyDomainName.INFRASTRUCTURE, "Infraestructura"))
        ValidateTechnologyComponent(TechnologyComponent("C1", "SRV-10001", "Server", "D1", EvidenceState=EvidenceState.AVAILABLE))
        ValidateBusinessService(BusinessService("S1", "Pagos", "EquipoPagos", EnterpriseRiskSeverity.HIGH))
        ValidateServiceComponentMap(ServiceComponentMap("M1", "S1", "C1", "Application", 80))

    def test_rechaza_impact_weight_fuera_de_rango(self):
        with self.assertRaises(ValidationError):
            ValidateServiceComponentMap(ServiceComponentMap("M1", "S1", "C1", "Application", 101))

    def test_evidencia_faltante_no_declara_lifecycle_conocido(self):
        Component = TechnologyComponent("C1", "SRV-10001", "Server", "D1", LifecycleStatus="Current", EvidenceState=EvidenceState.MISSING)
        with self.assertRaises(ValidationError):
            ValidateTechnologyComponent(Component)


if __name__ == "__main__":
    unittest.main()
