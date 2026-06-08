import unittest

from CapacityEngine.Application.ServiceCatalogService import ServiceCatalogService
from CapacityEngine.Domain.Entities import Service
from CapacityEngine.Domain.Exceptions import ValidationError


class ServiceCatalogContractTest(unittest.TestCase):
    def test_service_requires_owner_and_supported_criticality(self):
        with self.assertRaises(ValidationError):
            ServiceCatalogService().ValidateService(Service("S1", "Payments", "", "Invalid"))


if __name__ == "__main__":
    unittest.main()
