import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def RunScript(*Args):
    Env = os.environ.copy()
    Env["STACK_DRY_RUN"] = "1"
    return subprocess.run(Args, cwd=ROOT, env=Env, text=True, capture_output=True)


class ObservabilityContractTest(unittest.TestCase):
    def test_status_capacity_engine_batch_completado_es_saludable(self):
        Result = self.RunStatusWithFakePodman("0")
        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("salud: completado correctamente", Result.stdout)

    def test_status_capacity_engine_batch_fallido_reporta_error(self):
        Result = self.RunStatusWithFakePodman("2")
        self.assertNotEqual(Result.returncode, 0)
        self.assertIn("salud: fallo batch (exit code 2)", Result.stdout)

    def RunStatusWithFakePodman(self, ExitCode):
        with tempfile.TemporaryDirectory() as TempDir:
            Podman = Path(TempDir) / "podman"
            Podman.write_text(
                "#!/usr/bin/env bash\n"
                "set -eu\n"
                "if [ \"$1\" = \"container\" ] && [ \"$2\" = \"exists\" ]; then exit 0; fi\n"
                "if [ \"$1\" = \"inspect\" ] && [ \"$2\" = \"-f\" ]; then\n"
                "  if [ \"$3\" = \"{{.State.Running}}\" ]; then echo false; exit 0; fi\n"
                f"  if [ \"$3\" = \"{{{{.State.ExitCode}}}}\" ]; then echo {ExitCode}; exit 0; fi\n"
                "fi\n"
                "echo \"podman inesperado: $*\" >&2\n"
                "exit 2\n",
                encoding="utf-8",
            )
            Podman.chmod(0o755)
            Env = os.environ.copy()
            Env["PODMAN_BIN"] = str(Podman)
            return subprocess.run(
                ["bash", "Scripts/StackStatus.sh", "CapacityEngine"],
                cwd=ROOT,
                env=Env,
                text=True,
                capture_output=True,
            )

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
