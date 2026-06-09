import unittest

from CapacityEngine.Application.SyntheticDataService import SyntheticDataService


class EnterpriseTestingDataCoverageTest(unittest.TestCase):
    def test_datos_de_testing_incluyen_licencias_y_backlevel(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("EnterpriseTesting001", "mixed", "medium", 90, 42)
        Components = Dataset["EnterpriseComponents"]

        self.assertTrue(any(Component["LicenseStatus"] == "NonCompliant" for Component in Components))
        self.assertTrue(any(Component["BacklevelStatus"] == "Backlevel" for Component in Components))
        self.assertTrue(any(Component["LifecycleStatus"] == "EndOfSupport" for Component in Components))
        self.assertTrue(any(Component["ComplianceStatus"] == "AttentionRequired" for Component in Components))

    def test_riesgos_de_testing_incluyen_compliance_y_lifecycle(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("EnterpriseTesting002", "mixed", "medium", 90, 43)
        Categories = {Risk["RiskCategory"] for Risk in Dataset["EnterpriseRiskRegistry"]}

        self.assertIn("Compliance", Categories)
        self.assertIn("Lifecycle", Categories)


if __name__ == "__main__":
    unittest.main()
