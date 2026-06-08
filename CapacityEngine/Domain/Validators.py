from datetime import datetime
from typing import Iterable

from CapacityEngine.Domain.Constants import MetricName, ResourceType
from CapacityEngine.Domain.Entities import AlertThreshold, MetricSample, MonitoredResource, Service, ServiceResourceMap
from CapacityEngine.Domain.Exceptions import ValidationError


def RequireText(Value: str | None, FieldName: str) -> str:
    if Value is None or not str(Value).strip():
        raise ValidationError(f"{FieldName} is required")
    return str(Value).strip()


def RequirePositive(Value: float | None, FieldName: str) -> float:
    if Value is None or float(Value) <= 0:
        raise ValidationError(f"{FieldName} must be positive")
    return float(Value)


def ValidateService(ServiceValue: Service) -> None:
    RequireText(ServiceValue.ServiceId, "ServiceId")
    RequireText(ServiceValue.Name, "Name")
    RequireText(ServiceValue.Owner, "Owner")
    if ServiceValue.Criticality not in {"Low", "Medium", "High", "Critical"}:
        raise ValidationError("Criticality is unsupported")


def ValidateResource(Resource: MonitoredResource) -> None:
    RequireText(Resource.ResourceId, "ResourceId")
    RequireText(Resource.Name, "Name")
    if not isinstance(Resource.ResourceType, ResourceType):
        raise ValidationError("ResourceType is unsupported")
    RequireText(Resource.CapacityUnit, "CapacityUnit")
    if Resource.TotalCapacity is not None and Resource.TotalCapacity <= 0:
        raise ValidationError("TotalCapacity must be positive")


def ValidateServiceResourceMap(MapValue: ServiceResourceMap) -> None:
    RequireText(MapValue.ServiceId, "ServiceId")
    RequireText(MapValue.ResourceId, "ResourceId")
    if MapValue.ImpactWeight < 1 or MapValue.ImpactWeight > 100:
        raise ValidationError("ImpactWeight must be between 1 and 100")


def ValidateMetricSample(Sample: MetricSample) -> None:
    RequireText(Sample.MetricSampleId, "MetricSampleId")
    RequireText(Sample.ResourceId, "ResourceId")
    if not isinstance(Sample.MetricName, MetricName):
        raise ValidationError("MetricName is unsupported")
    if not isinstance(Sample.ObservedAt, datetime):
        raise ValidationError("ObservedAt must be a datetime")
    if Sample.Value < 0:
        raise ValidationError("Value must be non-negative")


def ValidateThreshold(Threshold: AlertThreshold) -> None:
    if Threshold.WarningValue < 0 or Threshold.CriticalValue < 0:
        raise ValidationError("Threshold values must be non-negative")
    if Threshold.Comparison in {"GreaterThan", "GreaterOrEqual"} and Threshold.CriticalValue < Threshold.WarningValue:
        raise ValidationError("Critical threshold must be greater than warning threshold")
    if Threshold.Comparison in {"LessThan", "LessOrEqual"} and Threshold.CriticalValue > Threshold.WarningValue:
        raise ValidationError("Critical threshold must be less than warning threshold")


def RejectDuplicateSamples(Samples: Iterable[MetricSample]) -> None:
    Seen = set()
    for Sample in Samples:
        Key = (Sample.ResourceId, Sample.MetricName.value, Sample.Source, Sample.ObservedAt)
        if Key in Seen:
            raise ValidationError("Duplicate metric sample")
        Seen.add(Key)
