import unittest

from CapacityEngine.Adapters.SyntheticPostgreSqlAdapter import SyntheticPostgreSqlAdapter
from CapacityEngine.Application.SyntheticDataService import SyntheticDataService


class EnterpriseDatasetContractTest(unittest.TestCase):
    def test_dataset_enterprise_incluye_scores_riesgos_y_recomendaciones(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("EnterpriseDemo001", "mixed", "small", 90, 1)
        self.assertIn("EnterpriseScores", Dataset)
        self.assertIn("EnterpriseRiskRegistry", Dataset)
        self.assertIn("EnterpriseRecommendations", Dataset)
        self.assertTrue(Dataset["EnterpriseScores"])
        self.assertTrue(Dataset["EnterpriseRiskRegistry"])

    def test_sql_enterprise_incluye_tablas_de_score_y_riesgo(self):
        Dataset = SyntheticDataService().BuildSyntheticDataset("EnterpriseSql001", "mixed", "small", 90, 1)
        Sql = SyntheticPostgreSqlAdapter().BuildLoadSql(Dataset)
        self.assertIn("create table if not exists EnterpriseScoreAssessment", Sql)
        self.assertIn("insert into EnterpriseRiskRegistryEntry", Sql)
        self.assertIn("TechnologyHealth", Sql)


if __name__ == "__main__":
    unittest.main()
