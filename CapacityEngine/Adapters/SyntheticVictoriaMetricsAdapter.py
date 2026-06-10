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
        self.DeleteRemoteSamples(LoadId)
        return Count

    def DeleteAll(self) -> int:
        Store = self.LoadStore()
        Count = sum(len(Samples) for Samples in Store.values())
        LoadIds = list(Store.keys())
        self.SaveStore({})
        for LoadId in LoadIds:
            self.DeleteRemoteSamples(LoadId)
        return Count

    def HasSamples(self, LoadId: str | None = None) -> bool:
        Store = self.LoadStore()
        if LoadId:
            return bool(Store.get(LoadId))
        return any(Store.values())

    def ImportSamples(self, Samples: list[dict]) -> None:
        Series = {}
        for Sample in Samples:
            Metric = {
                "__name__": self.NormalizeMetricName(Sample["MetricName"]),
                "load_id": Sample["LoadId"],
                "resource_id": Sample["ResourceId"],
                "host_name": Sample.get("HostName", Sample["ResourceId"]),
                "environment": Sample.get("Environment", "Unknown"),
                "technology_domain": Sample.get("TechnologyDomain", "Infrastructure"),
                "business_service": Sample.get("BusinessService", "Unknown"),
                "business_service_id": Sample.get("BusinessServiceId", "Unknown"),
                "source": Sample["Source"],
            }
            Key = json.dumps(Metric, sort_keys=True)
            Series.setdefault(Key, {"metric": Metric, "values": [], "timestamps": []})
            Series[Key]["values"].append(float(Sample["Value"]))
            Series[Key]["timestamps"].append(self.TimestampMillis(Sample["ObservedAt"]))
        Body = (
            "\n".join(json.dumps(Value, sort_keys=True) for Value in Series.values()) + "\n"
        ).encode("utf-8")
        Request = request.Request(
            f"{self.BaseUrl}/api/v1/import",
            data=Body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with request.urlopen(Request, timeout=10) as Response:
            if Response.status >= 300:
                raise RuntimeError(f"VictoriaMetrics rechazo la carga: HTTP {Response.status}")

    def BuildImportPayload(self, Samples: list[dict]) -> str:
        Series = {}
        for Sample in Samples:
            Metric = {
                "__name__": self.NormalizeMetricName(Sample["MetricName"]),
                "load_id": Sample["LoadId"],
                "resource_id": Sample["ResourceId"],
                "host_name": Sample.get("HostName", Sample["ResourceId"]),
                "environment": Sample.get("Environment", "Unknown"),
                "technology_domain": Sample.get("TechnologyDomain", "Infrastructure"),
                "business_service": Sample.get("BusinessService", "Unknown"),
                "business_service_id": Sample.get("BusinessServiceId", "Unknown"),
                "source": Sample["Source"],
            }
            Key = json.dumps(Metric, sort_keys=True)
            Series.setdefault(Key, {"metric": Metric, "values": [], "timestamps": []})
            Series[Key]["values"].append(float(Sample["Value"]))
            Series[Key]["timestamps"].append(self.TimestampMillis(Sample["ObservedAt"]))
        return "\n".join(json.dumps(Value, sort_keys=True) for Value in Series.values()) + "\n"

    def DeleteRemoteSamples(self, LoadId: str) -> None:
        if os.environ.get("STACK_DRY_RUN", "0") == "1":
            return
        Body = urlencode(
            {
                "match[]": [
                    f'synthetic_cpu{{load_id="{LoadId}"}}',
                    f'synthetic_ram{{load_id="{LoadId}"}}',
                    f'synthetic_storage{{load_id="{LoadId}"}}',
                    f'synthetic_iops{{load_id="{LoadId}"}}',
                    f'synthetic_network{{load_id="{LoadId}"}}',
                    f'synthetic_latency{{load_id="{LoadId}"}}',
                    f'synthetic_throughput{{load_id="{LoadId}"}}',
                    f'synthetic_errors{{load_id="{LoadId}"}}',
                    f'synthetic_saturation{{load_id="{LoadId}"}}',
                ]
            },
            doseq=True,
        ).encode("utf-8")
        Request = request.Request(
            f"{self.BaseUrl}/api/v1/admin/tsdb/delete_series",
            data=Body,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with request.urlopen(Request, timeout=10) as Response:
            if Response.status >= 300:
                raise RuntimeError(f"VictoriaMetrics rechazo el borrado: HTTP {Response.status}")

    def QueryHasSamples(self, LoadId: str | None = None) -> bool:
        Query = 'count_over_time(synthetic_cpu[400d])'
        if LoadId:
            Query = f'count_over_time(synthetic_cpu{{load_id="{LoadId}"}}[400d])'
        Url = f"{self.BaseUrl}/api/v1/query?{urlencode({'query': Query})}"
        with request.urlopen(Url, timeout=10) as Response:
            Payload = json.loads(Response.read().decode("utf-8"))
        Results = Payload.get("data", {}).get("result", [])
        for Result in Results:
            Value = Result.get("value", [None, "0"])[1]
            try:
                if float(Value) > 0:
                    return True
            except (TypeError, ValueError):
                continue
        return False

    def NormalizeMetricName(self, MetricName: str) -> str:
        return "synthetic_" + "".join(Character.lower() if Character.isalnum() else "_" for Character in MetricName)

    def TimestampMillis(self, ObservedAt: str) -> int:
        return int(datetime.fromisoformat(ObservedAt).timestamp() * 1000)

    def HasRemoteSamples(self, LoadId: str | None = None) -> bool:
        if os.environ.get("STACK_DRY_RUN", "0") == "1":
            return self.HasSamples(LoadId)
        return self.QueryHasSamples(LoadId)

    def LoadStore(self) -> dict:
        if not self.DataPath.exists():
            return {}
        return json.loads(self.DataPath.read_text(encoding="utf-8"))

    def SaveStore(self, Store: dict) -> None:
        self.DataDir.mkdir(parents=True, exist_ok=True)
        self.DataPath.write_text(json.dumps(Store, indent=2, sort_keys=True), encoding="utf-8")
