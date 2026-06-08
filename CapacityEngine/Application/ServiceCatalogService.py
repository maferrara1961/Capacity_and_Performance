from CapacityEngine.Domain.Constants import RiskLevel
from CapacityEngine.Domain.Entities import Application, MonitoredResource, Service, ServiceResourceMap
from CapacityEngine.Domain.Exceptions import ValidationError
from CapacityEngine.Domain.Validators import ValidateResource, ValidateService, ValidateServiceResourceMap


class ServiceCatalogService:
    def ValidateService(self, ServiceValue: Service) -> None:
        ValidateService(ServiceValue)

    def ValidateResource(self, Resource: MonitoredResource) -> None:
        ValidateResource(Resource)

    def ValidateMapping(self, MapValue: ServiceResourceMap, Services: list[Service], Resources: list[MonitoredResource]) -> None:
        ValidateServiceResourceMap(MapValue)
        ServiceIds = {Item.ServiceId for Item in Services}
        ResourceIds = {Item.ResourceId for Item in Resources}
        if MapValue.ServiceId not in ServiceIds:
            raise ValidationError("Mapping references nonexistent service")
        if MapValue.ResourceId not in ResourceIds:
            raise ValidationError("Mapping references nonexistent resource")

    def IsComplete(self, ServiceValue: Service, Maps: list[ServiceResourceMap]) -> bool:
        return bool(ServiceValue.Owner and ServiceValue.Criticality and any(MapValue.ServiceId == ServiceValue.ServiceId for MapValue in Maps))

    def ApplicationRiskFromDependencies(self, DependencyRisks: list[RiskLevel]) -> RiskLevel:
        if RiskLevel.CRITICAL in DependencyRisks:
            return RiskLevel.CRITICAL
        if RiskLevel.WARNING in DependencyRisks:
            return RiskLevel.WARNING
        if RiskLevel.UNKNOWN in DependencyRisks:
            return RiskLevel.UNKNOWN
        return RiskLevel.OK
