import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def RunScript(*Args):
    Env = os.environ.copy()
    Env["STACK_DRY_RUN"] = "1"
    return subprocess.run(Args, cwd=ROOT, env=Env, text=True, capture_output=True)


class BuildImagesContractTest(unittest.TestCase):
    def test_build_total_valida_containerfiles_y_resume(self):
        Result = RunScript("bash", "Scripts/BuildImages.sh")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("resumen de build", Result.stdout)
        self.assertIn("capacity-performance-grafana:latest", Result.stdout)

    def test_build_individual_grafana_con_version(self):
        Result = RunScript("bash", "Scripts/BuildImages.sh", "Grafana", "v1.0.0")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("capacity-performance-grafana:v1.0.0", Result.stdout)

    def test_rechaza_servicio_invalido(self):
        Result = RunScript("bash", "Scripts/BuildImages.sh", "Invalido")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("servicio no permitido", Result.stderr)

    def test_rechaza_version_vacia(self):
        Result = RunScript("bash", "Scripts/BuildImages.sh", "Grafana", "")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("version", Result.stderr)


if __name__ == "__main__":
    unittest.main()
