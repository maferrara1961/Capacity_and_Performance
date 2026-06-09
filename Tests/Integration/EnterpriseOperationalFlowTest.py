import unittest

from CapacityEngine.Adapters.SyntheticVictoriaMetricsAdapter import SyntheticVictoriaMetricsAdapter
from CapacityEngine.Application.SyntheticDataService import SyntheticDataService


class EnterpriseOperationalFlowTest(unittest.TestCase):
    def test_dataset_historico_incluye_labels_enterprise(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("EnterpriseFlow001", "mixed", "small", 90, 1234)
        Payload = SyntheticVictoriaMetricsAdapter().BuildImportPayload(Dataset["Samples"])

        self.assertIn("EnterpriseScores", Dataset)
        self.assertIn("technology_domain", Payload)
        self.assertIn("business_service", Payload)
        self.assertIn("host_name", Payload)


if __name__ == "__main__":
    unittest.main()
