import unittest

from CapacityEngine.Application.ServiceCatalogService import ServiceCatalogService
from CapacityEngine.Domain.Constants import ResourceType
from CapacityEngine.Domain.Entities import MonitoredResource, Service, ServiceResourceMap
from CapacityEngine.Domain.Exceptions import ValidationError


class ServiceCatalogValidationTest(unittest.TestCase):
    def test_completeness_and_mapping_validation(self):
        Catalog = ServiceCatalogService()
        ServiceValue = Service("S1", "Payments", "Ops", "Critical")
        Resource = MonitoredResource("R1", ResourceType.SERVER, "server-a", "Linux", "Percent", 100)
        Mapping = ServiceResourceMap("M1", "S1", "R1", "Primary", 90)
        Catalog.ValidateMapping(Mapping, [ServiceValue], [Resource])
        self.assertTrue(Catalog.IsComplete(ServiceValue, [Mapping]))

    def test_rejects_unknown_resource_mapping(self):
        Catalog = ServiceCatalogService()
        ServiceValue = Service("S1", "Payments", "Ops", "Critical")
        Mapping = ServiceResourceMap("M1", "S1", "Missing", "Primary", 90)
        with self.assertRaises(ValidationError):
            Catalog.ValidateMapping(Mapping, [ServiceValue], [])


if __name__ == "__main__":
    unittest.main()
