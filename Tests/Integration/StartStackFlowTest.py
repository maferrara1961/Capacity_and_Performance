import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class StartStackFlowTest(unittest.TestCase):
    def test_start_informa_dependencias_y_mensajes_en_castellano(self):
        Env = os.environ.copy()
        Env["STACK_DRY_RUN"] = "1"
        Result = subprocess.run(["bash", "Scripts/StartStack.sh"], cwd=ROOT, env=Env, text=True, capture_output=True)
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("validando dependencias de Grafana", Result.stdout)
        self.assertIn("stack iniciado", Result.stdout)


if __name__ == "__main__":
    unittest.main()
