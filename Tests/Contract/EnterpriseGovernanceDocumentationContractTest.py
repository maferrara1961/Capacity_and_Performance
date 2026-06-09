import unittest
from pathlib import Path


class EnterpriseGovernanceDocumentationContractTest(unittest.TestCase):
    def test_documentacion_enterprise_declara_evidencia_scores_y_dashboards(self):
        Text = Path("docs/EnterpriseGovernancePlatform.md").read_text(encoding="utf-8")
        for Expected in [
            "Plataforma Enterprise de Gobierno",
            "TechnologyHealth",
            "Available",
            "Missing",
            "Enterprise Executive Dashboard",
            "Scripts/RunEnterpriseAssessment.sh",
        ]:
            self.assertIn(Expected, Text)

    def test_readme_referencia_gobierno_enterprise(self):
        Text = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("Gobierno Enterprise", Text)
        self.assertIn("Enterprise Executive Dashboard", Text)


if __name__ == "__main__":
    unittest.main()
