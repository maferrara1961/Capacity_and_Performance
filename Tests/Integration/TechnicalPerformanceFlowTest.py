import unittest

from CapacityEngine.Adapters.VictoriaMetricsAdapter import VictoriaMetricsAdapter
from CapacityEngine.Application.SyntheticDataService import SyntheticDataService


class TechnicalPerformanceFlowTest(unittest.TestCase):
    def test_metric_query_maps_resource_filter(self):
        Query = VictoriaMetricsAdapter().MetricQuery("CPU", "ResourceA")
        self.assertIn('resource_id="ResourceA"', Query)

    def test_warning_and_mixed_profiles_include_required_performance_metrics(self):
        Required = {"CPU", "RAM", "Storage", "IOPS", "Network", "Latency", "Throughput", "Errors", "Saturation"}
        for Profile in ["warning", "mixed"]:
            Dataset = SyntheticDataService().BuildSyntheticDataset(f"Technical{Profile}001", Profile, "small", 90, 1)
            Metrics = {Sample["MetricName"] for Sample in Dataset["Samples"]}
            self.assertTrue(Required.issubset(Metrics))
            self.assertTrue(all("ResourceId" in Sample for Sample in Dataset["Samples"]))


if __name__ == "__main__":
    unittest.main()
