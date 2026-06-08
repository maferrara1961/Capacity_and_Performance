from urllib.parse import urlencode


class VictoriaMetricsAdapter:
    def __init__(self, BaseUrl: str = "http://victoriametrics:8428") -> None:
        self.BaseUrl = BaseUrl.rstrip("/")

    def BuildQueryUrl(self, Query: str) -> str:
        return f"{self.BaseUrl}/api/v1/query?{urlencode({'query': Query})}"

    def MetricQuery(self, MetricName: str, ResourceId: str) -> str:
        return f'{MetricName}{{resource_id="{ResourceId}"}}'
