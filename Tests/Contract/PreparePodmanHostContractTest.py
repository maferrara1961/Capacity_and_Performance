import subprocess
import unittest
from pathlib import Path


class PreparePodmanHostContractTest(unittest.TestCase):
    def setUp(self):
        self.RepoRoot = Path(__file__).resolve().parents[2]
        self.ScriptPath = self.RepoRoot / "Scripts" / "PreparePodmanHost.sh"

    def test_dry_run_validates_host_preparation_without_podman(self):
        Result = subprocess.run(
            ["bash", str(self.ScriptPath)],
            cwd=self.RepoRoot,
            env={"STACK_DRY_RUN": "1", "PATH": "/usr/bin:/bin"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(Result.returncode, 0, Result.stderr)
        self.assertIn("preparacion de host validada", Result.stdout)

    def test_script_documents_linger_requirement(self):
        Content = self.ScriptPath.read_text(encoding="utf-8")

        self.assertIn("loginctl enable-linger", Content)
        self.assertIn("podman system renumber", Content)
        self.assertIn("contenedores rootless", Content)


if __name__ == "__main__":
    unittest.main()
