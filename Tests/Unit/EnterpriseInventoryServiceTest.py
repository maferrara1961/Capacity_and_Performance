import unittest

from CapacityEngine.Application.EnterpriseInventoryService import EnterpriseInventoryService
from CapacityEngine.Domain.EnterpriseConstants import TechnologyDomainName
from CapacityEngine.Domain.EnterpriseEntities import BusinessService, TechnologyComponent, TechnologyDomain


class EnterpriseInventoryServiceTest(unittest.TestCase):
    def test_mapea_componentes_por_servicio(self):
        Service = EnterpriseInventoryService()
        Components = [
            TechnologyComponent("C1", "SRV-10001", "Server", "D1", BusinessServiceId="S1"),
            TechnologyComponent("C2", "SRV-10002", "Database", "D1", BusinessServiceId="S1"),
        ]
        Services = [BusinessService("S1", "Pagos", "CapacityLab")]

        Result = Service.MapComponentsToServices(Components, Services)

        self.assertEqual(["SRV-10001", "SRV-10002"], [Item.ComponentName for Item in Result["S1"]])

    def test_identifica_componentes_sin_servicio(self):
        Service = EnterpriseInventoryService()
        Components = [
            TechnologyComponent("C1", "SRV-10001", "Server", "D1"),
            TechnologyComponent("C2", "SRV-10002", "Database", "D1", BusinessServiceId="S1"),
        ]

        Result = Service.ComponentsWithoutService(Components)

        self.assertEqual(["SRV-10001"], [Item.ComponentName for Item in Result])

    def test_construye_dominio_tecnologico(self):
        Service = EnterpriseInventoryService()

        Domain = Service.BuildDomain("D1", TechnologyDomainName.INFRASTRUCTURE, "Infraestructura")

        self.assertIsInstance(Domain, TechnologyDomain)
        self.assertEqual(TechnologyDomainName.INFRASTRUCTURE, Domain.Name)


if __name__ == "__main__":
    unittest.main()
