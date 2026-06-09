from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
import re

from CapacityEngine.Domain.Exceptions import ValidationError


AllowedProfiles = {"normal", "warning", "critical", "overprovisioned", "underprovisioned", "mixed"}
AllowedVolumes = {"small", "medium", "large"}
AllowedStatuses = {"Planned", "Running", "Succeeded", "Failed", "PartiallyDeleted", "Deleted"}
AllowedTransitions = {
    "Planned": {"Running", "Failed"},
    "Running": {"Succeeded", "Failed"},
    "Succeeded": {"PartiallyDeleted", "Deleted"},
    "PartiallyDeleted": {"Deleted"},
    "Failed": {"Deleted"},
    "Deleted": set(),
}


def ValidateLoadId(Value: str | None) -> str:
    if Value is None or not str(Value).strip():
        raise ValidationError("el identificador de lote es requerido")
    CleanValue = str(Value).strip()
    if len(CleanValue) > 64 or not re.fullmatch(r"[A-Za-z0-9_-]+", CleanValue):
        raise ValidationError("el identificador de lote solo permite letras, numeros, guion y guion bajo")
    return CleanValue


def ValidateProfile(Value: str | None) -> str:
    CleanValue = str(Value or "mixed").strip().lower()
    if CleanValue not in AllowedProfiles:
        raise ValidationError("perfil no permitido")
    return CleanValue


def ValidateVolume(Value: str | None) -> str:
    CleanValue = str(Value or "small").strip().lower()
    if CleanValue not in AllowedVolumes:
        raise ValidationError("volumen no permitido")
    return CleanValue


def ValidateDays(Value: str | int | None) -> int:
    if Value is None:
        return 90
    try:
        Days = int(Value)
    except (TypeError, ValueError) as Error:
        raise ValidationError("dias debe ser un numero positivo") from Error
    if Days < 1 or Days > 366:
        raise ValidationError("dias debe estar entre 1 y 366")
    return Days


def ValidateSeed(Value: str | int | None) -> int | None:
    if Value is None:
        return None
    try:
        Seed = int(Value)
    except (TypeError, ValueError) as Error:
        raise ValidationError("seed debe ser un numero positivo") from Error
    if Seed < 0:
        raise ValidationError("seed debe ser un numero positivo")
    return Seed


def ValidateStatus(Value: str) -> str:
    if Value not in AllowedStatuses:
        raise ValidationError("estado de lote no permitido")
    return Value


@dataclass(frozen=True)
class TestLoad:
    LoadId: str
    ScenarioProfile: str
    RequestedVolume: str
    CreatedAt: str = ""
    FinishedAt: str = ""
    Status: str = "Planned"
    GeneratedServiceCount: int = 0
    GeneratedResourceCount: int = 0
    GeneratedMetricSampleCount: int = 0
    GeneratedKpiCount: int = 0
    GeneratedForecastCount: int = 0
    GeneratedRiskCount: int = 0
    GeneratedRecommendationCount: int = 0
    ErrorMessage: str = ""
    IsTestData: bool = True

    @staticmethod
    def Create(LoadId: str, ScenarioProfile: str, RequestedVolume: str) -> "TestLoad":
        return TestLoad(
            LoadId=ValidateLoadId(LoadId),
            ScenarioProfile=ValidateProfile(ScenarioProfile),
            RequestedVolume=ValidateVolume(RequestedVolume),
            CreatedAt=datetime.now(UTC).isoformat(),
        )

    def WithStatus(self, Status: str, ErrorMessage: str = "") -> "TestLoad":
        Status = ValidateStatus(Status)
        if Status not in AllowedTransitions[self.Status]:
            raise ValidationError(f"transicion de lote no permitida: {self.Status} -> {Status}")
        FinishedAt = datetime.now(UTC).isoformat() if Status in {"Succeeded", "Failed", "Deleted"} else self.FinishedAt
        return replace(self, Status=Status, FinishedAt=FinishedAt, ErrorMessage=ErrorMessage)

    def WithCounts(self, Services: int, Resources: int, Samples: int, Kpis: int, Forecasts: int, Risks: int, Recommendations: int) -> "TestLoad":
        return replace(
            self,
            GeneratedServiceCount=Services,
            GeneratedResourceCount=Resources,
            GeneratedMetricSampleCount=Samples,
            GeneratedKpiCount=Kpis,
            GeneratedForecastCount=Forecasts,
            GeneratedRiskCount=Risks,
            GeneratedRecommendationCount=Recommendations,
        )

    def ToDict(self) -> dict:
        return asdict(self)

    @staticmethod
    def FromDict(Value: dict) -> "TestLoad":
        return TestLoad(**Value)


@dataclass(frozen=True)
class ToolValidationResult:
    ToolName: str
    Target: str
    Protocol: str
    Status: str
    Message: str
    ValidatedAt: str


def ValidateTestLoad(Load: TestLoad) -> None:
    ValidateLoadId(Load.LoadId)
    ValidateProfile(Load.ScenarioProfile)
    ValidateVolume(Load.RequestedVolume)
    ValidateStatus(Load.Status)
    if not Load.IsTestData:
        raise ValidationError("la carga debe estar marcada como dato de prueba")


def BuildToolValidationResult(ToolName: str, Target: str, Protocol: str, Available: bool, Message: str) -> ToolValidationResult:
    return ToolValidationResult(
        ToolName=ToolName,
        Target=Target,
        Protocol=Protocol,
        Status="Available" if Available else "Unavailable",
        Message=Message,
        ValidatedAt=datetime.now(UTC).isoformat(),
    )
