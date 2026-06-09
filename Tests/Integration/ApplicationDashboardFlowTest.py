import unittest

from CapacityEngine.Application.SyntheticDataService import SyntheticDataService
from CapacityEngine.Application.ServiceCatalogService import ServiceCatalogService
from CapacityEngine.Domain.Constants import RiskLevel


class ApplicationDashboardFlowTest(unittest.TestCase):
    def test_dependency_risk_propagates_to_application(self):
        Risk = ServiceCatalogService().ApplicationRiskFromDependencies([RiskLevel.OK, RiskLevel.CRITICAL])
        self.assertEqual(Risk, RiskLevel.CRITICAL)

    def test_synthetic_service_context_maps_resources_to_services(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("ApplicationMixed001", "mixed", "small", 90, 1)
        ServiceIds = {Service["ServiceId"] for Service in Dataset["Services"]}
        ResourceIds = {Resource["ResourceId"] for Resource in Dataset["Resources"]}
        self.assertTrue(ServiceIds)
        self.assertTrue(ResourceIds)


if __name__ == "__main__":
    unittest.main()
