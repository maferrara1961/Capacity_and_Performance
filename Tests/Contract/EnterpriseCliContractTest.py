import unittest
from pathlib import Path


class EnterpriseCliContractTest(unittest.TestCase):
    def test_cli_declara_comandos_enterprise(self):
        Text = Path("CapacityEngine/Scheduler/SyntheticDataCommand.py").read_text(encoding="utf-8")
        self.assertIn("sync-enterprise-inventory", Text)
        self.assertIn("run-enterprise-assessment", Text)
        self.assertIn("validate-enterprise-governance", Text)
        self.assertIn("generate-enterprise-verification-data", Text)

    def test_scripts_enterprise_existen(self):
        for Script in [
            "Scripts/RunEnterpriseAssessment.sh",
            "Scripts/ValidateEnterpriseGovernance.sh",
            "Scripts/GenerateEnterpriseVerificationData.sh",
        ]:
            Text = Path(Script).read_text(encoding="utf-8")
            self.assertIn("SyntheticDataCommand", Text)


if __name__ == "__main__":
    unittest.main()
