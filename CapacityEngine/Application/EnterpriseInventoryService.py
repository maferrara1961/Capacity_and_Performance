from CapacityEngine.Domain.EnterpriseConstants import TechnologyDomainName
from CapacityEngine.Domain.EnterpriseEntities import BusinessService, TechnologyComponent, TechnologyDomain
from CapacityEngine.Domain.Validators import RequireText


class EnterpriseInventoryService:
    def BuildDomain(self, DomainId: str, Name: TechnologyDomainName, Description: str) -> TechnologyDomain:
        return TechnologyDomain(RequireText(DomainId, "DomainId"), Name, RequireText(Description, "Description"))

    def MapComponentsToServices(self, Components: list[TechnologyComponent], Services: list[BusinessService]) -> dict[str, list[TechnologyComponent]]:
        KnownServiceIds = {Service.BusinessServiceId for Service in Services}
        Result = {Service.BusinessServiceId: [] for Service in Services}
        for Component in Components:
            if Component.BusinessServiceId in KnownServiceIds:
                Result[Component.BusinessServiceId].append(Component)
        return Result

    def ComponentsWithoutService(self, Components: list[TechnologyComponent]) -> list[TechnologyComponent]:
        return [Component for Component in Components if not Component.BusinessServiceId]

    def BuildComponentsFromZabbixHosts(self, Hosts: list[dict]) -> list[TechnologyComponent]:
        Components = []
        for Host in Hosts:
            HostName = RequireText(Host.get("HostName"), "HostName")
            Components.append(
                TechnologyComponent(
                    ComponentId=f"Zabbix{Host.get('HostId', HostName)}",
                    ComponentName=HostName,
                    TechnologyType=Host.get("Type") or "Server",
                    DomainId="DomainInfrastructure",
                    Version=Host.get("Os") or "Unknown",
                    Vendor="ZabbixInventory",
                    Environment=Host.get("Location") or "Unknown",
                    Owner="CapacityLab",
                    SupportStatus=Host.get("Status") or "Unknown",
                    LifecycleStatus="Unknown",
                )
            )
        return Components
