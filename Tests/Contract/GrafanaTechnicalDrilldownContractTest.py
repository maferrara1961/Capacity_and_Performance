import json
import unittest
from pathlib import Path


class GrafanaTechnicalDrilldownContractTest(unittest.TestCase):
    def setUp(self):
        self.RepoRoot = Path(__file__).resolve().parents[2]
        self.DashboardRoot = self.RepoRoot / "Config" / "Grafana" / "Dashboards"

    def test_links_to_technical_performance_pass_dashboard_load_variable(self):
        BrokenLinks = []

        for DashboardPath in self.DashboardRoot.rglob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Link in self.FindLinks(Dashboard):
                Url = Link.get("url", "")
                if "/d/technical-performance/technical-performance-dashboard" not in Url:
                    continue
                if "var-LoadId=${LoadId}" in Url:
                    BrokenLinks.append(f"{DashboardPath.name}: {Url}")

        self.assertEqual([], BrokenLinks)

    def test_links_to_technical_performance_include_host_or_service_context(self):
        MissingContext = []

        for DashboardPath in self.DashboardRoot.rglob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Link in self.FindLinks(Dashboard):
                Url = Link.get("url", "")
                if "/d/technical-performance/technical-performance-dashboard" not in Url:
                    continue
                if "var-HostName=" not in Url or "var-ServiceId=" not in Url:
                    MissingContext.append(f"{DashboardPath.name}: {Url}")

        self.assertEqual([], MissingContext)

    def FindLinks(self, Value):
        if isinstance(Value, dict):
            if "url" in Value:
                yield Value
            for Child in Value.values():
                yield from self.FindLinks(Child)
        elif isinstance(Value, list):
            for Child in Value:
                yield from self.FindLinks(Child)


if __name__ == "__main__":
    unittest.main()
