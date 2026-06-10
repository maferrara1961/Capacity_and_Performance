import json
import unittest
from pathlib import Path


class GrafanaTechnicalDrilldownContractTest(unittest.TestCase):
    def setUp(self):
        self.RepoRoot = Path(__file__).resolve().parents[2]
        self.DashboardRoot = self.RepoRoot / "Config" / "Grafana" / "Dashboards"

    def test_links_to_technical_performance_do_not_pass_literal_dashboard_variable_name(self):
        BrokenLinks = []

        for DashboardPath in self.DashboardRoot.rglob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Link in self.FindLinks(Dashboard):
                Url = Link.get("url", "")
                if "/d/technical-performance/technical-performance-dashboard" not in Url:
                    continue
                if "var-LoadId=${var-LoadId}" in Url:
                    BrokenLinks.append(f"{DashboardPath.name}: {Url}")

        self.assertEqual([], BrokenLinks)

    def test_panels_without_host_field_do_not_send_empty_host_filter(self):
        BrokenLinks = []

        for DashboardPath in self.DashboardRoot.rglob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Panel in Dashboard.get("panels", []):
                TargetText = json.dumps(Panel.get("targets", []))
                if "HostName" in TargetText or "host_name" in TargetText:
                    continue
                for Link in self.FindLinks(Panel):
                    Url = Link.get("url", "")
                    if "/d/technical-performance/technical-performance-dashboard" not in Url:
                        continue
                    if "var-HostName=${__data.fields.HostName}" in Url:
                        BrokenLinks.append(f"{DashboardPath.name}: {Panel.get('title')}: {Url}")

        self.assertEqual([], BrokenLinks)

    def test_table_links_use_grafana_field_index_syntax(self):
        BrokenLinks = []

        for DashboardPath in self.DashboardRoot.rglob("*.json"):
            Dashboard = json.loads(DashboardPath.read_text(encoding="utf-8"))
            for Link in self.FindLinks(Dashboard):
                Url = Link.get("url", "")
                if "/d/technical-performance/technical-performance-dashboard" not in Url:
                    continue
                if "${__data.fields." in Url:
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
