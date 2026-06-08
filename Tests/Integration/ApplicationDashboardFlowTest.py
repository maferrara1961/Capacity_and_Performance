import unittest

from CapacityEngine.Application.ServiceCatalogService import ServiceCatalogService
from CapacityEngine.Domain.Constants import RiskLevel


class ApplicationDashboardFlowTest(unittest.TestCase):
    def test_dependency_risk_propagates_to_application(self):
        Risk = ServiceCatalogService().ApplicationRiskFromDependencies([RiskLevel.OK, RiskLevel.CRITICAL])
        self.assertEqual(Risk, RiskLevel.CRITICAL)


if __name__ == "__main__":
    unittest.main()
