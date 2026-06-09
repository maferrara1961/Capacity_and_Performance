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
        self.AgentFactPath = self.DataDir / "ZabbixAgent" / "EnterpriseFacts.tsv"
        self.BaseUrl = (BaseUrl or os.environ.get("ZABBIX_URL", "http://localhost:8080/api_jsonrpc.php")).rstrip("/")
        self.User = os.environ.get("ZABBIX_USER", "Admin")
        self.Password = os.environ.get("ZABBIX_PASSWORD", "zabbix")
        self.AgentDns = os.environ.get("ZABBIX_AGENT_DNS", "capacity-performance-zabbix-agent")

    def SaveDataset(self, LoadId: str, Dataset: dict) -> None:
        Store = self.LoadStore()
        Store[LoadId] = {
            "Hosts": [Resource["Name"] for Resource in Dataset["Resources"]],
            "Samples": len(Dataset["Samples"]),
        }
        self.SaveAgentFacts(Dataset)
        self.SaveStore(Store)
        if os.environ.get("STACK_DRY_RUN", "0") != "1":
            self.ImportDataset(Dataset)

    def DeleteDataset(self, LoadId: str) -> int:
        Store = self.LoadStore()
        Record = Store.pop(LoadId, None)
        self.DeleteAgentFactsForHosts((Record or {}).get("Hosts", []))
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
        self.SaveAgentFactsFile({})
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
        EnterpriseByHost = self.EnterpriseComponentsByHost(Dataset)
        ItemIdsByResourceMetric = {}
        for Resource in Dataset["Resources"]:
            HostId = self.EnsureHost(Token, GroupId, Resource)
            InterfaceId = self.EnsureAgentInterface(Token, HostId)
            self.EnsureEnterpriseAgentItems(Token, HostId, InterfaceId, Resource["Name"], EnterpriseByHost.get(Resource["Name"], {}))
            ItemIds = []
            for Sample in LatestSamples.get(Resource["ResourceId"], {}).values():
                ItemId = self.EnsureItem(Token, HostId, Sample)
                ItemIds.append(ItemId)
                ItemIdsByResourceMetric[(Resource["ResourceId"], Sample["MetricName"])] = ItemId
                self.EnsureTriggers(Token, Resource["Name"], Resource["Name"], Sample)
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

    def SaveAgentFacts(self, Dataset: dict) -> None:
        CurrentFacts = self.LoadAgentFacts()
        for Component in Dataset.get("EnterpriseComponents", []):
            CurrentFacts[Component["ComponentName"]] = {
                "LicenseStatus": Component.get("LicenseStatus", "Unknown"),
                "ComplianceStatus": Component.get("ComplianceStatus", "Unknown"),
                "BacklevelStatus": Component.get("BacklevelStatus", "Unknown"),
                "LifecycleStatus": Component.get("LifecycleStatus", "Unknown"),
                "EndOfSupportDate": Component.get("EndOfSupportDate", "Unknown"),
            }
        self.AgentFactPath.parent.mkdir(parents=True, exist_ok=True)
        Header = ["HostName", "LicenseStatus", "ComplianceStatus", "BacklevelStatus", "LifecycleStatus", "EndOfSupportDate"]
        Lines = ["\t".join(Header)]
        for HostName in sorted(CurrentFacts):
            Facts = CurrentFacts[HostName]
            Lines.append("\t".join([HostName] + [Facts.get(Field, "Unknown") for Field in Header[1:]]))
        self.AgentFactPath.write_text("\n".join(Lines) + "\n", encoding="utf-8")

    def SaveAgentFactsFile(self, FactsByHost: dict) -> None:
        self.AgentFactPath.parent.mkdir(parents=True, exist_ok=True)
        Header = ["HostName", "LicenseStatus", "ComplianceStatus", "BacklevelStatus", "LifecycleStatus", "EndOfSupportDate"]
        Lines = ["\t".join(Header)]
        for HostName in sorted(FactsByHost):
            Facts = FactsByHost[HostName]
            Lines.append("\t".join([HostName] + [Facts.get(Field, "Unknown") for Field in Header[1:]]))
        self.AgentFactPath.write_text("\n".join(Lines) + "\n", encoding="utf-8")

    def DeleteAgentFactsForHosts(self, HostNames: list[str]) -> None:
        if not HostNames:
            return
        Facts = self.LoadAgentFacts()
        for HostName in HostNames:
            Facts.pop(HostName, None)
        self.SaveAgentFactsFile(Facts)

    def LoadAgentFacts(self) -> dict:
        if not self.AgentFactPath.exists():
            return {}
        Lines = self.AgentFactPath.read_text(encoding="utf-8").splitlines()
        if not Lines:
            return {}
        Header = Lines[0].split("\t")
        Facts = {}
        for Line in Lines[1:]:
            Values = Line.split("\t")
            Row = dict(zip(Header, Values))
            HostName = Row.pop("HostName", "")
            if HostName:
                Facts[HostName] = Row
        return Facts

    def EnterpriseComponentsByHost(self, Dataset: dict) -> dict:
        return {Component["ComponentName"]: Component for Component in Dataset.get("EnterpriseComponents", [])}

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
        Hosts = self.ApiCall(
            Token,
            "host.get",
            {
                "output": ["hostid"],
                "selectInventory": ["asset_tag"],
                "searchInventory": {"asset_tag": f"{LoadId}-"},
            },
        )
        HostIds = [Host["hostid"] for Host in Hosts]
        if HostIds:
            self.ApiCall(Token, "host.delete", HostIds)

    def HasRemoteData(self, LoadId: str | None = None) -> bool:
        Token = self.Login()
        Params = {"output": ["hostid"], "selectInventory": ["asset_tag"], "search": {"host": "SRV-"}}
        if LoadId:
            Params = {"output": ["hostid"], "selectInventory": ["asset_tag"], "searchInventory": {"asset_tag": f"{LoadId}-"}}
        Hosts = self.ApiCall(Token, "host.get", Params)
        return bool(Hosts)

    def ListInventoryHosts(self) -> list[dict]:
        if os.environ.get("STACK_DRY_RUN", "0") == "1":
            return self.ListStoredInventoryHosts()
        Token = self.Login()
        Hosts = self.ApiCall(
            Token,
            "host.get",
            {
                "output": ["hostid", "host", "name", "status"],
                "selectInventory": ["asset_tag", "alias", "type", "os", "location", "notes"],
                "search": {"host": "SRV-"},
            },
        )
        return [self.NormalizeInventoryHost(Host) for Host in Hosts]

    def ListEnterpriseInventoryComponents(self) -> list[dict]:
        Components = []
        for Host in self.ListInventoryHosts():
            Components.append(
                {
                    "HostId": Host["HostId"],
                    "HostName": Host["HostName"],
                    "VisibleName": Host["HostName"],
                    "Status": Host["Status"],
                    "AssetTag": Host["AssetTag"],
                    "Type": Host["Type"],
                    "Os": Host["Os"],
                    "Location": Host["Location"],
                    "Notes": Host["Notes"],
                    "TechnologyDomain": "Infrastructure",
                    "BusinessService": "Servicio inventariado desde Zabbix",
                    "InventorySource": "Zabbix",
                }
            )
        return Components

    def ListStoredInventoryHosts(self) -> list[dict]:
        Store = self.LoadStore()
        Hosts = []
        for LoadId, Record in Store.items():
            for Index, HostName in enumerate(Record.get("Hosts", []), start=1):
                Hosts.append(
                    {
                        "HostId": f"dryrun-{LoadId}-{Index}",
                        "HostName": HostName,
                        "VisibleName": HostName,
                        "Status": "OK",
                        "AssetTag": f"{LoadId}-{Index}",
                        "Type": "Server",
                        "Os": "Linux",
                        "Location": "CapacityLab",
                        "Notes": "Host sintetico en modo simulacion",
                    }
                )
        return Hosts

    def NormalizeInventoryHost(self, Host: dict) -> dict:
        Inventory = Host.get("inventory") or {}
        Status = "Disabled" if str(Host.get("status", "0")) == "1" else "OK"
        HostName = Host.get("host") or Host.get("name")
        return {
            "HostId": Host.get("hostid", ""),
            "HostName": HostName,
            "VisibleName": Host.get("name") or HostName,
            "Status": Status,
            "AssetTag": Inventory.get("asset_tag") or HostName,
            "Type": Inventory.get("type") or "Server",
            "Os": Inventory.get("os") or "Unknown",
            "Location": Inventory.get("location") or "Unknown",
            "Notes": Inventory.get("notes") or "",
        }

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
        Existing = self.ApiCall(Token, "host.get", {"output": ["hostid"], "filter": {"host": [Resource["Name"]]}})
        if Existing:
            self.UpdateHostInventory(Token, Existing[0]["hostid"], Resource)
            return Existing[0]["hostid"]
        Created = self.ApiCall(
            Token,
            "host.create",
            {
                "host": Resource["Name"],
                "name": Resource["Name"],
                "groups": [{"groupid": GroupId}],
                "interfaces": [self.AgentInterfaceDefinition()],
                "inventory_mode": 0,
                "inventory": self.BuildZabbixInventory(Resource),
            },
        )
        return Created["hostids"][0]

    def AgentInterfaceDefinition(self) -> dict:
        return {
            "type": 1,
            "main": 1,
            "useip": 0,
            "ip": "",
            "dns": self.AgentDns,
            "port": "10050",
        }

    def EnsureAgentInterface(self, Token: str, HostId: str) -> str:
        Existing = self.ApiCall(Token, "hostinterface.get", {"output": ["interfaceid", "dns", "type"], "hostids": HostId})
        for Interface in Existing:
            if str(Interface.get("type")) == "1":
                return Interface["interfaceid"]
        Created = self.ApiCall(Token, "hostinterface.create", {"hostid": HostId, **self.AgentInterfaceDefinition()})
        return Created["interfaceids"][0]

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

    def EnsureEnterpriseAgentItems(self, Token: str, HostId: str, InterfaceId: str, HostName: str, Component: dict) -> None:
        Facts = [
            ("LicenseStatus", "Licencia - Estado", "license_status"),
            ("ComplianceStatus", "Compliance - Estado", "compliance_status"),
            ("BacklevelStatus", "Software Backlevel - Estado", "backlevel_status"),
            ("LifecycleStatus", "Lifecycle - Estado", "lifecycle_status"),
            ("EndOfSupportDate", "Software - Fecha fin de soporte", "end_of_support_date"),
        ]
        for FactName, ItemName, KeySuffix in Facts:
            Key = f"capacity.enterprise.fact[{HostName},{FactName}]"
            Existing = self.ApiCall(Token, "item.get", {"output": ["itemid"], "hostids": HostId, "filter": {"key_": [Key]}})
            if Existing:
                continue
            self.ApiCall(
                Token,
                "item.create",
                {
                    "hostid": HostId,
                    "interfaceid": InterfaceId,
                    "name": f"Enterprise {ItemName}",
                    "key_": Key,
                    "type": 0,
                    "value_type": 4,
                    "delay": "1h",
                    "history": "90d",
                    "trends": "0",
                    "description": f"Dato levantado por Zabbix Agent desde inventario enterprise sintetico: {KeySuffix}. Valor esperado inicial: {Component.get(FactName, 'Unknown')}",
                },
            )

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
