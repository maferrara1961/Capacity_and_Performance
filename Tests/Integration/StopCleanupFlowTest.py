import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class StopCleanupFlowTest(unittest.TestCase):
    def test_cleanup_confirmado_elimina_temporales_en_modo_simulacion(self):
        Env = os.environ.copy()
        Env["STACK_DRY_RUN"] = "1"
        Result = subprocess.run(["bash", "Scripts/CleanupStack.sh", "--confirmar"], cwd=ROOT, env=Env, text=True, capture_output=True)
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("eliminando red temporal", Result.stdout)


if __name__ == "__main__":
    unittest.main()
