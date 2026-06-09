import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SyntheticDataFlowTest(unittest.TestCase):
    def setUp(self):
        self.Env = os.environ.copy()
        self.Env["SYNTHETIC_DATA_DIR"] = tempfile.mkdtemp(prefix="synthetic-flow-")
        self.Env["STACK_DRY_RUN"] = "1"

    def RunManage(self, *Args):
        return subprocess.run(["bash", "Scripts/ManageTestData.sh", *Args], cwd=ROOT, env=self.Env, text=True, capture_output=True)

    def test_carga_lista_valida_y_borra_lotes(self):
        First = self.RunManage("load", "--profile", "normal", "--volume", "small", "--load-id", "DemoNormal001")
        Second = self.RunManage("load", "--profile", "critical", "--volume", "small", "--load-id", "DemoCritical001")
        self.assertEqual(First.returncode, 0, First.stderr)
        self.assertEqual(Second.returncode, 0, Second.stderr)

        Listed = self.RunManage("list")
        self.assertIn("DemoNormal001", Listed.stdout)
        self.assertIn("DemoCritical001", Listed.stdout)

        Validated = self.RunManage("validate", "--load-id", "DemoCritical001")
        self.assertEqual(Validated.returncode, 0, Validated.stderr)
        self.assertIn("validacion sintetica completada", Validated.stdout)

        Deleted = self.RunManage("delete", "--load-id", "DemoNormal001")
        self.assertEqual(Deleted.returncode, 0, Deleted.stderr)
        AfterDelete = self.RunManage("list")
        self.assertNotIn("DemoNormal001 Succeeded", AfterDelete.stdout)
        self.assertIn("DemoCritical001", AfterDelete.stdout)

        DeleteAll = self.RunManage("delete", "--all", "--confirmar")
        self.assertEqual(DeleteAll.returncode, 0, DeleteAll.stderr)
        Final = self.RunManage("list")
        self.assertIn("sin cargas sinteticas", Final.stdout)


if __name__ == "__main__":
    unittest.main()
