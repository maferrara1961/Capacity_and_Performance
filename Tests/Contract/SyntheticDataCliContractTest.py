import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def RunManage(*Args):
    Env = os.environ.copy()
    Env["SYNTHETIC_DATA_DIR"] = tempfile.mkdtemp(prefix="synthetic-contract-")
    Env["STACK_DRY_RUN"] = "1"
    return subprocess.run(["bash", "Scripts/ManageTestData.sh", *Args], cwd=ROOT, env=Env, text=True, capture_output=True)


class SyntheticDataCliContractTest(unittest.TestCase):
    def test_load_imprime_resumen_en_castellano(self):
        Result = RunManage("load", "--profile", "mixed", "--volume", "small", "--load-id", "DemoLoad001")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("INFO: carga sintetica completada", Result.stdout)
        self.assertIn("lote: DemoLoad001", Result.stdout)
        self.assertIn("servicios:", Result.stdout)
        self.assertIn("recomendaciones:", Result.stdout)

    def test_rechaza_profile_invalido(self):
        Result = RunManage("load", "--profile", "invalido")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("perfil no permitido", Result.stderr)

    def test_delete_all_requiere_confirmacion(self):
        Result = RunManage("delete", "--all")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("--confirmar", Result.stderr)

    def test_validate_imprime_herramientas(self):
        Result = RunManage("validate")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("Grafana", Result.stdout)
        self.assertIn("VictoriaMetrics", Result.stdout)
        self.assertIn("PostgreSQL", Result.stdout)


if __name__ == "__main__":
    unittest.main()
