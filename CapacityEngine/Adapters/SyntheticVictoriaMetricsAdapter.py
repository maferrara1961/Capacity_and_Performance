import json
import os
from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode
from urllib import request


class SyntheticVictoriaMetricsAdapter:
    def __init__(self, DataDir: str | None = None, BaseUrl: str | None = None) -> None:
        self.DataDir = Path(DataDir or os.environ.get("SYNTHETIC_DATA_DIR", ".capacity-test-data"))
        self.DataPath = self.DataDir / "VictoriaMetricsSamples.json"
        self.BaseUrl = (BaseUrl or os.environ.get("VICTORIAMETRICS_URL", "http://localhost:8428")).rstrip("/")

    def SaveSamples(self, LoadId: str, Samples: list[dict]) -> None:
        Store = self.LoadStore()
        Store[LoadId] = Samples
        self.SaveStore(Store)
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            self.ImportSamples(Samples)

    def DeleteSamples(self, LoadId: str) -> int:
        Store = self.LoadStore()
        Count = len(Store.pop(LoadId, []))
        self.SaveStore(Store)
        return Count

    def DeleteAll(self) -> int:
        Store = self.LoadStore()
        Count = sum(len(Samples) for Samples in Store.values())
        self.SaveStore({})
        return Count

    def HasSamples(self, LoadId: str | None = None) -> bool:
        Store = self.LoadStore()
        if LoadId:
            return bool(Store.get(LoadId))
        return any(Store.values())

    def ImportSamples(self, Samples: list[dict]) -> None:
        Lines = []
        for Sample in Samples:
            MetricName = self.NormalizeMetricName(Sample["MetricName"])
            Labels = (
                f'load_id="{Sample["LoadId"]}",'
                f'resource_id="{Sample["ResourceId"]}",'
                f'source="{Sample["Source"]}"'
            )
            Lines.append(f'{MetricName}{{{Labels}}} {Sample["Value"]} {self.TimestampMillis(Sample["ObservedAt"])}')
        Body = ("\n".join(Lines) + "\n").encode("utf-8")
        Request = request.Request(
            f"{self.BaseUrl}/api/v1/import/prometheus",
            data=Body,
            method="POST",
            headers={"Content-Type": "text/plain"},
        )
        with request.urlopen(Request, timeout=10) as Response:
            if Response.status >= 300:
                raise RuntimeError(f"VictoriaMetrics rechazo la carga: HTTP {Response.status}")

    def NormalizeMetricName(self, MetricName: str) -> str:
        return "synthetic_" + "".join(Character.lower() if Character.isalnum() else "_" for Character in MetricName)

    def TimestampMillis(self, ObservedAt: str) -> int:
        return int(datetime.fromisoformat(ObservedAt).timestamp() * 1000)

    def HasRemoteSamples(self, LoadId: str | None = None) -> bool:
        if os.environ.get("STACK_DRY_RUN", "0") == "1":
            return self.HasSamples(LoadId)
        Query = 'synthetic_cpu'
        if LoadId:
            Query = f'synthetic_cpu{{load_id="{LoadId}"}}'
        Url = f"{self.BaseUrl}/api/v1/query?{urlencode({'query': Query})}"
        with request.urlopen(Url, timeout=10) as Response:
            Payload = json.loads(Response.read().decode("utf-8"))
        return bool(Payload.get("data", {}).get("result"))

    def LoadStore(self) -> dict:
        if not self.DataPath.exists():
            return {}
        return json.loads(self.DataPath.read_text(encoding="utf-8"))

    def SaveStore(self, Store: dict) -> None:
        self.DataDir.mkdir(parents=True, exist_ok=True)
        self.DataPath.write_text(json.dumps(Store, indent=2, sort_keys=True), encoding="utf-8")
