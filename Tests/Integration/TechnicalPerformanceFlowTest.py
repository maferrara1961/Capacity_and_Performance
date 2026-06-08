import unittest

from CapacityEngine.Adapters.VictoriaMetricsAdapter import VictoriaMetricsAdapter


class TechnicalPerformanceFlowTest(unittest.TestCase):
    def test_metric_query_maps_resource_filter(self):
        Query = VictoriaMetricsAdapter().MetricQuery("CPU", "ResourceA")
        self.assertIn('resource_id="ResourceA"', Query)


if __name__ == "__main__":
    unittest.main()
