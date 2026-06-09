import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LocalAccessContractTest(unittest.TestCase):
    def test_validate_local_access_simula_protocolos_correctos(self):
        Env = os.environ.copy()
        Env["STACK_DRY_RUN"] = "1"
        Result = subprocess.run(
            ["bash", "Scripts/ValidateLocalAccess.sh", "127.0.0.1"],
            cwd=ROOT,
            env=Env,
            text=True,
            capture_output=True,
        )
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("validando HTTP Grafana", Result.stdout)
        self.assertIn("validando HTTP Zabbix Web", Result.stdout)
        self.assertIn("validando HTTP VictoriaMetrics", Result.stdout)
        self.assertIn("validando TCP PostgreSQL", Result.stdout)
        self.assertIn("validando TCP Zabbix Server", Result.stdout)
        self.assertIn("validacion local de acceso completada correctamente", Result.stdout)


if __name__ == "__main__":
    unittest.main()
