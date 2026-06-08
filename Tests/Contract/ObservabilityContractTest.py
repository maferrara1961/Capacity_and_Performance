import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def RunScript(*Args):
    Env = os.environ.copy()
    Env["STACK_DRY_RUN"] = "1"
    return subprocess.run(Args, cwd=ROOT, env=Env, text=True, capture_output=True)


class ObservabilityContractTest(unittest.TestCase):
    def test_logs_de_servicio_permitido(self):
        Result = RunScript("bash", "Scripts/StackLogs.sh", "Grafana", "10")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("mostrando ultimas 10 lineas de Grafana", Result.stdout)

    def test_logs_rechaza_servicio_inexistente(self):
        Result = RunScript("bash", "Scripts/StackLogs.sh", "NoExiste", "10")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("servicio no permitido", Result.stderr)

    def test_status_stack_completo(self):
        Result = RunScript("bash", "Scripts/StackStatus.sh")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("estado de PostgreSQL", Result.stdout)
        self.assertIn("estado de CapacityEngine", Result.stdout)

    def test_logs_rechaza_lineas_invalidas(self):
        Result = RunScript("bash", "Scripts/StackLogs.sh", "Grafana", "cero")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("lineas", Result.stderr)


if __name__ == "__main__":
    unittest.main()
