import json
import os
from pathlib import Path

from CapacityEngine.Domain.SyntheticData import TestLoad


class SyntheticPostgreSqlAdapter:
    def __init__(self, DataDir: str | None = None) -> None:
        self.DataDir = Path(DataDir or os.environ.get("SYNTHETIC_DATA_DIR", ".capacity-test-data"))
        self.DataPath = self.DataDir / "TestLoads.json"

    def LoadStore(self) -> dict:
        if not self.DataPath.exists():
            return {"Loads": {}, "Datasets": {}}
        return json.loads(self.DataPath.read_text(encoding="utf-8"))

    def SaveStore(self, Store: dict) -> None:
        self.DataDir.mkdir(parents=True, exist_ok=True)
        self.DataPath.write_text(json.dumps(Store, indent=2, sort_keys=True), encoding="utf-8")

    def SaveDataset(self, Dataset: dict) -> None:
        Store = self.LoadStore()
        LoadId = Dataset["Load"]["LoadId"]
        if LoadId in Store["Loads"] and Store["Loads"][LoadId]["Status"] != "Deleted":
            raise ValueError("el identificador de lote ya existe")
        Store["Loads"][LoadId] = Dataset["Load"]
        Store["Datasets"][LoadId] = Dataset
        self.SaveStore(Store)

    def ListLoads(self, Status: str | None = None) -> list[TestLoad]:
        Store = self.LoadStore()
        Loads = [TestLoad.FromDict(Value) for Value in Store["Loads"].values() if Value.get("Status") != "Deleted"]
        if Status:
            Loads = [Load for Load in Loads if Load.Status == Status]
        return sorted(Loads, key=lambda Load: Load.CreatedAt)

    def GetDataset(self, LoadId: str) -> dict | None:
        return self.LoadStore()["Datasets"].get(LoadId)

    def DeleteLoad(self, LoadId: str) -> int:
        Store = self.LoadStore()
        Dataset = Store["Datasets"].pop(LoadId, None)
        if LoadId in Store["Loads"]:
            Store["Loads"][LoadId] = TestLoad.FromDict(Store["Loads"][LoadId]).WithStatus("Deleted").ToDict()
        self.SaveStore(Store)
        return self.CountRecords(Dataset)

    def DeleteAll(self) -> tuple[int, int]:
        Store = self.LoadStore()
        LoadIds = [LoadId for LoadId, Load in Store["Loads"].items() if Load.get("IsTestData") and Load.get("Status") != "Deleted"]
        RecordCount = 0
        for LoadId in LoadIds:
            RecordCount += self.CountRecords(Store["Datasets"].pop(LoadId, None))
            Store["Loads"][LoadId] = TestLoad.FromDict(Store["Loads"][LoadId]).WithStatus("Deleted").ToDict()
        self.SaveStore(Store)
        return len(LoadIds), RecordCount

    def CountRecords(self, Dataset: dict | None) -> int:
        if not Dataset:
            return 0
        return sum(len(Value) for Key, Value in Dataset.items() if Key != "Load" and isinstance(Value, list)) + 1

    def HasData(self, LoadId: str | None = None) -> bool:
        if LoadId:
            return self.GetDataset(LoadId) is not None
        return bool(self.ListLoads())
