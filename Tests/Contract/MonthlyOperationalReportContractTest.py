import subprocess
import unittest
from pathlib import Path

from CapacityEngine.Scheduler.MonthlyOperationalReport import MonthlyOperationalReport


class MonthlyOperationalReportContractTest(unittest.TestCase):
    def test_script_and_module_define_operational_report(self) -> None:
        Script = Path("Scripts/GenerateMonthlyOperationalReport.sh")
        Module = Path("CapacityEngine/Scheduler/MonthlyOperationalReport.py")

        self.assertTrue(Script.exists())
        self.assertTrue(Module.exists())

        Source = Module.read_text(encoding="utf-8")
        self.assertIn("Reporte Operativo Mensual", Source)
        self.assertIn("Anomalias Detectadas", Source)
        self.assertIn("Sugerencias Priorizadas", Source)
        self.assertIn("synthetic_cpu", Source)
        self.assertIn("synthetic_ram", Source)
        self.assertIn("platform_container_up", Source)

    def test_month_validation_rejects_invalid_format(self) -> None:
        Report = MonthlyOperationalReport()

        with self.assertRaises(ValueError):
            Report.ValidateMonth("2026/06")

    def test_cli_help_is_available(self) -> None:
        Result = subprocess.run(
            ["python3", "-m", "CapacityEngine.Scheduler.MonthlyOperationalReport", "--help"],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(Result.returncode, 0)
        self.assertIn("--month", Result.stdout)
        self.assertIn("--load-id", Result.stdout)
