import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib import request


class SyntheticZabbixAdapter:
    def __init__(self, DataDir: str | None = None, BaseUrl: str | None = None) -> None:
        self.DataDir = Path(DataDir or os.environ.get("SYNTHETIC_DATA_DIR", ".capacity-test-data"))
        self.DataPath = self.DataDir / "ZabbixObjects.json"
        self.BaseUrl = (BaseUrl or os.environ.get("ZABBIX_URL", "http://localhost:8080/api_jsonrpc.php")).rstrip("/")
        self.User = os.environ.get("ZABBIX_USER", "Admin")
        self.Password = os.environ.get("ZABBIX_PASSWORD", "zabbix")

    def SaveDataset(self, LoadId: str, Dataset: dict) -> None:
        Store = self.LoadStore()
        Store[LoadId] = {
            "Hosts": [Resource["ResourceId"] for Resource in Dataset["Resources"]],
            "Samples": len(Dataset["Samples"]),
        }
        self.SaveStore(Store)
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            self.ImportDataset(Dataset)

    def DeleteDataset(self, LoadId: str) -> int:
        Store = self.LoadStore()
        Record = Store.pop(LoadId, None)
        self.SaveStore(Store)
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            self.DeleteRemoteDataset(LoadId)
        if not Record:
            return 0
        return len(Record.get("Hosts", [])) + int(Record.get("Samples", 0))

    def DeleteAll(self) -> int:
        Store = self.LoadStore()
        LoadIds = list(Store.keys())
        Count = sum(len(Record.get("Hosts", [])) + int(Record.get("Samples", 0)) for Record in Store.values())
        self.SaveStore({})
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            for LoadId in LoadIds:
                self.DeleteRemoteDataset(LoadId)
        return Count

    def HasData(self, LoadId: str | None = None) -> bool:
        if os.environ.get("STACK_DRY_RUN", "0") == "1":
            Store = self.LoadStore()
            if LoadId:
                return LoadId in Store
            return bool(Store)
        return self.HasRemoteData(LoadId)

    def ImportDataset(self, Dataset: dict) -> None:
        Token = self.Login()
        GroupId = self.EnsureHostGroup(Token, "Capacity Synthetic")
        LatestSamples = self.LatestSamplesByResourceAndMetric(Dataset["Samples"])
        ItemIdsByResourceMetric = {}
        for Resource in Dataset["Resources"]:
            HostId = self.EnsureHost(Token, GroupId, Resource)
            ItemIds = []
            for Sample in LatestSamples.get(Resource["ResourceId"], {}).values():
                ItemId = self.EnsureItem(Token, HostId, Sample)
                ItemIds.append(ItemId)
                ItemIdsByResourceMetric[(Resource["ResourceId"], Sample["MetricName"])] = ItemId
                self.EnsureTriggers(Token, Resource["ResourceId"], Resource["Name"], Sample)
            self.EnsureGraph(Token, HostId, Resource["Name"], ItemIds)
        History = self.BuildHistoryPushPayload(Dataset["Samples"], ItemIdsByResourceMetric)
        for Chunk in self.Chunks(History, 100):
            Result = self.ApiCall(Token, "history.push", Chunk)
            Errors = [Item for Item in Result.get("data", []) if Item.get("error")]
            if Errors:
                print(
                    "WARN: Zabbix creo hosts/items sinteticos, pero rechazo algunas muestras "
                    f"historicas: {Errors[0]['error']}",
                    file=sys.stderr,
                )
                return

    def BuildHistoryPushPayload(self, Samples: list[dict], ItemIdsByResourceMetric: dict[tuple[str, str], str]) -> list[dict]:
        History = []
        for Sample in Samples:
            ItemId = ItemIdsByResourceMetric.get((Sample["ResourceId"], Sample["MetricName"]))
            if ItemId:
                History.append(
                    {
                        "itemid": ItemId,
                        "value": Sample["Value"],
                        "clock": self.TimestampSeconds(Sample["ObservedAt"]),
                        "ns": 0,
                    }
                )
        return History

    def DeleteRemoteDataset(self, LoadId: str) -> None:
        Token = self.Login()
        Hosts = self.ApiCall(Token, "host.get", {"output": ["hostid"], "search": {"host": f"{LoadId}-Resource-"}})
        HostIds = [Host["hostid"] for Host in Hosts]
        if HostIds:
            self.ApiCall(Token, "host.delete", HostIds)

    def HasRemoteData(self, LoadId: str | None = None) -> bool:
        Token = self.Login()
        Search = {"host": f"{LoadId}-Resource-"} if LoadId else {"host": "-Resource-"}
        Hosts = self.ApiCall(Token, "host.get", {"output": ["hostid"], "search": Search})
        return bool(Hosts)

    def Login(self) -> str:
        Result = self.ApiCall(None, "user.login", {"username": self.User, "password": self.Password})
        if not isinstance(Result, str) or not Result:
            raise RuntimeError("Zabbix no devolvio token de autenticacion")
        return Result

    def EnsureHostGroup(self, Token: str, Name: str) -> str:
        Existing = self.ApiCall(Token, "hostgroup.get", {"output": ["groupid"], "filter": {"name": [Name]}})
        if Existing:
            return Existing[0]["groupid"]
        Created = self.ApiCall(Token, "hostgroup.create", {"name": Name})
        return Created["groupids"][0]

    def EnsureHost(self, Token: str, GroupId: str, Resource: dict) -> str:
        Existing = self.ApiCall(Token, "host.get", {"output": ["hostid"], "filter": {"host": [Resource["ResourceId"]]}})
        if Existing:
            self.UpdateHostInventory(Token, Existing[0]["hostid"], Resource)
            return Existing[0]["hostid"]
        Created = self.ApiCall(
            Token,
            "host.create",
            {
                "host": Resource["ResourceId"],
                "name": Resource["Name"],
                "groups": [{"groupid": GroupId}],
                "inventory_mode": 0,
                "inventory": self.BuildZabbixInventory(Resource),
            },
        )
        return Created["hostids"][0]

    def UpdateHostInventory(self, Token: str, HostId: str, Resource: dict) -> None:
        self.ApiCall(
            Token,
            "host.update",
            {
                "hostid": HostId,
                "name": Resource["Name"],
                "inventory_mode": 0,
                "inventory": self.BuildZabbixInventory(Resource),
            },
        )

    def BuildZabbixInventory(self, Resource: dict) -> dict:
        Inventory = Resource.get("Inventory", {})
        return {
            "name": Resource["Name"],
            "alias": Inventory.get("Alias", Resource["Name"]),
            "asset_tag": Inventory.get("AssetTag", Resource["ResourceId"]),
            "type": Inventory.get("Type", Resource.get("ResourceType", "Server")),
            "os": Inventory.get("Os", "Linux"),
            "location": Inventory.get("Location", "CapacityLab"),
            "notes": Inventory.get("Notes", "Host sintetico de capacity"),
        }

    def EnsureItem(self, Token: str, HostId: str, Sample: dict) -> str:
        Key = self.ItemKey(Sample["MetricName"])
        Existing = self.ApiCall(Token, "item.get", {"output": ["itemid"], "hostids": HostId, "filter": {"key_": [Key]}})
        if Existing:
            return Existing[0]["itemid"]
        Created = self.ApiCall(
            Token,
            "item.create",
            {
                "hostid": HostId,
                "name": f"Capacity Synthetic {Sample['MetricName']}",
                "key_": Key,
                "type": 2,
                "value_type": 0,
                "delay": "0",
                "trends": "365d",
                "history": "90d",
            },
        )
        return Created["itemids"][0]

    def EnsureGraph(self, Token: str, HostId: str, ResourceName: str, ItemIds: list[str]) -> str | None:
        if not ItemIds:
            return None
        Name = f"Capacity Synthetic - {ResourceName}"
        Existing = self.ApiCall(Token, "graph.get", {"output": ["graphid"], "hostids": HostId, "filter": {"name": [Name]}})
        if Existing:
            return Existing[0]["graphid"]
        Colors = ["199C0D", "F2CC0C", "E24D42", "1F78C1", "BA43A9", "705DA0", "508642", "CCA300", "447EBC"]
        Created = self.ApiCall(
            Token,
            "graph.create",
            {
                "name": Name,
                "width": 900,
                "height": 200,
                "gitems": [
                    {
                        "itemid": ItemId,
                        "color": Colors[Index % len(Colors)],
                    }
                    for Index, ItemId in enumerate(ItemIds)
                ],
            },
        )
        return Created["graphids"][0]

    def EnsureTriggers(self, Token: str, HostKey: str, HostName: str, Sample: dict) -> None:
        Thresholds = self.TriggerThresholds(Sample["MetricName"])
        if not Thresholds:
            return
        Key = self.ItemKey(Sample["MetricName"])
        for SeverityName, Priority, Value in Thresholds:
            Description = f"Capacity Synthetic {SeverityName} {Sample['MetricName']} - {HostName}"
            Existing = self.ApiCall(Token, "trigger.get", {"output": ["triggerid"], "filter": {"description": [Description]}})
            if Existing:
                continue
            self.ApiCall(
                Token,
                "trigger.create",
                {
                    "description": Description,
                    "expression": f"last(/{HostKey}/{Key})>{Value}",
                    "priority": Priority,
                    "comments": f"Alerta sintetica de capacity para validar dashboards y graficas por host. Umbral {SeverityName}: {Value}.",
                },
            )

    def TriggerThresholds(self, MetricName: str) -> list[tuple[str, int, int]]:
        Thresholds = {
            "CPU": [("Warning", 2, 75), ("Critical", 4, 90)],
            "RAM": [("Warning", 2, 75), ("Critical", 4, 90)],
            "Storage": [("Warning", 2, 75), ("Critical", 4, 90)],
            "IOPS": [("Warning", 2, 75), ("Critical", 4, 90)],
            "Network": [("Warning", 2, 75), ("Critical", 4, 90)],
            "Saturation": [("Warning", 2, 70), ("Critical", 4, 85)],
            "Latency": [("Warning", 2, 70), ("Critical", 4, 90)],
            "Errors": [("Warning", 2, 5), ("Critical", 4, 10)],
        }
        return Thresholds.get(MetricName, [])

    def ApiCall(self, Token: str | None, Method: str, Params) -> object:
        Payload = {"jsonrpc": "2.0", "method": Method, "params": Params, "id": 1}
        Headers = {"Content-Type": "application/json"}
        if Token:
            Headers["Authorization"] = f"Bearer {Token}"
        Request = request.Request(
            self.BaseUrl,
            data=json.dumps(Payload).encode("utf-8"),
            method="POST",
            headers=Headers,
        )
        with request.urlopen(Request, timeout=20) as Response:
            Body = json.loads(Response.read().decode("utf-8"))
        if "error" in Body:
            Error = Body["error"]
            raise RuntimeError(f"Zabbix API {Method} fallo: {Error.get('data') or Error.get('message')}")
        return Body.get("result")

    def LatestSamplesByResourceAndMetric(self, Samples: list[dict]) -> dict:
        Latest = {}
        for Sample in Samples:
            ResourceSamples = Latest.setdefault(Sample["ResourceId"], {})
            Current = ResourceSamples.get(Sample["MetricName"])
            if not Current or Sample["ObservedAt"] > Current["ObservedAt"]:
                ResourceSamples[Sample["MetricName"]] = Sample
        return Latest

    def ItemKey(self, MetricName: str) -> str:
        Clean = "".join(Character.lower() if Character.isalnum() else "_" for Character in MetricName)
        return f"capacity.synthetic[{Clean}]"

    def TimestampSeconds(self, ObservedAt: str) -> int:
        return int(datetime.fromisoformat(ObservedAt).timestamp())

    def Chunks(self, Values: list, Size: int) -> list:
        for Index in range(0, len(Values), Size):
            yield Values[Index : Index + Size]

    def LoadStore(self) -> dict:
        if not self.DataPath.exists():
            return {}
        return json.loads(self.DataPath.read_text(encoding="utf-8"))

    def SaveStore(self, Store: dict) -> None:
        self.DataDir.mkdir(parents=True, exist_ok=True)
        self.DataPath.write_text(json.dumps(Store, indent=2, sort_keys=True), encoding="utf-8")
