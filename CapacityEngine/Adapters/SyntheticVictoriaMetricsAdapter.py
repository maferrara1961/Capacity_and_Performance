import json
import os
from pathlib import Path


class SyntheticVictoriaMetricsAdapter:
    def __init__(self, DataDir: str | None = None) -> None:
        self.DataDir = Path(DataDir or os.environ.get("SYNTHETIC_DATA_DIR", ".capacity-test-data"))
        self.DataPath = self.DataDir / "VictoriaMetricsSamples.json"

    def SaveSamples(self, LoadId: str, Samples: list[dict]) -> None:
        Store = self.LoadStore()
        Store[LoadId] = Samples
        self.SaveStore(Store)

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

    def LoadStore(self) -> dict:
        if not self.DataPath.exists():
            return {}
        return json.loads(self.DataPath.read_text(encoding="utf-8"))

    def SaveStore(self, Store: dict) -> None:
        self.DataDir.mkdir(parents=True, exist_ok=True)
        self.DataPath.write_text(json.dumps(Store, indent=2, sort_keys=True), encoding="utf-8")
