import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def RunScript(*Args):
    Env = os.environ.copy()
    Env["STACK_DRY_RUN"] = "1"
    return subprocess.run(Args, cwd=ROOT, env=Env, text=True, capture_output=True)


class LifecycleContractTest(unittest.TestCase):
    def test_start_respeta_orden_de_dependencias(self):
        Result = RunScript("bash", "Scripts/StartStack.sh")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        Output = Result.stdout
        self.assertLess(Output.index("iniciando PostgreSQL"), Output.index("iniciando Zabbix"))
        self.assertLess(Output.index("iniciando VictoriaMetrics"), Output.index("iniciando Grafana"))

    def test_start_crea_red_comun(self):
        Result = RunScript("bash", "Scripts/StartStack.sh")
        self.assertIn("red comun", Result.stdout)

    def test_stop_preserva_volumenes(self):
        Result = RunScript("bash", "Scripts/StopStack.sh")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("volumenes persistentes fueron preservados", Result.stdout)

    def test_cleanup_requiere_confirmacion(self):
        Result = RunScript("bash", "Scripts/CleanupStack.sh")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("--confirmar", Result.stderr)

    def test_cleanup_confirmado_no_borra_volumenes(self):
        Result = RunScript("bash", "Scripts/CleanupStack.sh", "--confirmar")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("no se eliminaron volumenes persistentes", Result.stdout)


if __name__ == "__main__":
    unittest.main()
