import argparse
import json
import math
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib import request
from urllib.parse import urlencode

from CapacityEngine.Adapters.SyntheticPostgreSqlAdapter import SyntheticPostgreSqlAdapter


MONTH_PATTERN = re.compile(r"^\d{4}-\d{2}$")


@dataclass
class MetricPoint:
    MetricName: str
    HostName: str
    Value: float


@dataclass
class Anomaly:
    HostName: str
    Category: str
    Severity: str
    Evidence: str
    Suggestion: str


class VictoriaMetricsReportClient:
    def __init__(self, BaseUrl: str | None = None) -> None:
        self.BaseUrl = (BaseUrl or os.environ.get("VICTORIAMETRICS_URL", "http://localhost:8428")).rstrip("/")

    def Query(self, QueryText: str) -> list[MetricPoint]:
        Url = f"{self.BaseUrl}/api/v1/query?{urlencode({'query': QueryText})}"
        with request.urlopen(Url, timeout=10) as Response:
            Payload = json.loads(Response.read().decode("utf-8"))
        Results = Payload.get("data", {}).get("result", [])
        Points: list[MetricPoint] = []
        for Result in Results:
            Metric = Result.get("metric", {})
            Value = Result.get("value", [None, "0"])[1]
            try:
                NumericValue = float(Value)
            except (TypeError, ValueError):
                continue
            HostName = Metric.get("host_name") or Metric.get("container") or Metric.get("resource_id") or "SinHost"
            MetricName = Metric.get("__name__", "metric")
            Points.append(MetricPoint(MetricName, HostName, NumericValue))
        return Points


class MonthlyOperationalReport:
    def __init__(self, Victoria: VictoriaMetricsReportClient | None = None, PostgreSql: SyntheticPostgreSqlAdapter | None = None) -> None:
        self.Victoria = Victoria or VictoriaMetricsReportClient()
        self.PostgreSql = PostgreSql or SyntheticPostgreSqlAdapter()

    def Build(self, Month: str, LoadId: str, OutputPath: Path) -> Path:
        self.ValidateMonth(Month)
        Days = self.EstimateDays(Month)
        GeneratedAt = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        MetricSummary, MetricErrors = self.CollectMetricSummary(LoadId, Days)
        Anomalies = self.BuildAnomalies(MetricSummary, MetricErrors)
        PostgreSqlRecommendations, PostgreSqlErrors = self.CollectPostgreSqlRecommendations(LoadId)

        Lines = [
            f"# Reporte Operativo Mensual - {Month}",
            "",
            f"- **Alcance:** `{LoadId}`",
            f"- **Periodo analizado:** {Month}",
            f"- **Generado:** {GeneratedAt}",
            "- **Regla de evidencia:** la ausencia de datos se informa como condicion desconocida, no como estado saludable.",
            "",
            "## Resumen Ejecutivo",
            "",
            self.BuildExecutiveSummary(Anomalies, MetricErrors, PostgreSqlErrors),
            "",
            "## Anomalias Detectadas",
            "",
            self.BuildAnomalyTable(Anomalies),
            "",
            "## Sugerencias Priorizadas",
            "",
            self.BuildSuggestionList(Anomalies),
            "",
            "## Evidencia de Capacidad y Performance",
            "",
            self.BuildMetricTable(MetricSummary),
            "",
            "## Riesgos y Recomendaciones desde PostgreSQL",
            "",
            self.BuildPostgreSqlTable(PostgreSqlRecommendations, PostgreSqlErrors),
            "",
            "## Calidad de Evidencia",
            "",
            self.BuildEvidenceQuality(MetricSummary, MetricErrors, PostgreSqlErrors),
            "",
        ]

        OutputPath.parent.mkdir(parents=True, exist_ok=True)
        OutputPath.write_text("\n".join(Lines), encoding="utf-8")
        return OutputPath

    def ValidateMonth(self, Month: str) -> None:
        if not MONTH_PATTERN.match(Month):
            raise ValueError("el mes debe tener formato YYYY-MM")
        try:
            datetime.strptime(Month, "%Y-%m")
        except ValueError as Error:
            raise ValueError("el mes debe tener formato YYYY-MM valido") from Error

    def EstimateDays(self, Month: str) -> int:
        Year, MonthNumber = [int(Part) for Part in Month.split("-")]
        if MonthNumber == 12:
            NextMonth = datetime(Year + 1, 1, 1)
        else:
            NextMonth = datetime(Year, MonthNumber + 1, 1)
        CurrentMonth = datetime(Year, MonthNumber, 1)
        return max(1, (NextMonth - CurrentMonth).days)

    def CollectMetricSummary(self, LoadId: str, Days: int) -> tuple[dict[str, dict[str, float]], list[str]]:
        Summary: dict[str, dict[str, float]] = {}
        Errors: list[str] = []
        MetricQueries = {
            "CPU promedio": f'avg_over_time(synthetic_cpu{{load_id=~"{LoadId}"}}[{Days}d])',
            "CPU pico": f'max_over_time(synthetic_cpu{{load_id=~"{LoadId}"}}[{Days}d])',
            "CPU p95": f'quantile_over_time(0.95, synthetic_cpu{{load_id=~"{LoadId}"}}[{Days}d])',
            "RAM promedio": f'avg_over_time(synthetic_ram{{load_id=~"{LoadId}"}}[{Days}d])',
            "RAM pico": f'max_over_time(synthetic_ram{{load_id=~"{LoadId}"}}[{Days}d])',
            "RAM p95": f'quantile_over_time(0.95, synthetic_ram{{load_id=~"{LoadId}"}}[{Days}d])',
            "Network pico": f'max_over_time(synthetic_network{{load_id=~"{LoadId}"}}[{Days}d])',
            "IOPS pico": f'max_over_time(synthetic_iops{{load_id=~"{LoadId}"}}[{Days}d])',
            "Disponibilidad minima": f'min_over_time(platform_container_up{{load_id=~"{LoadId}"}}[{Days}d])',
        }

        for MetricName, QueryText in MetricQueries.items():
            try:
                Points = self.Victoria.Query(QueryText)
            except Exception as Error:  # pragma: no cover - exercised against live stack
                Errors.append(f"{MetricName}: {Error}")
                continue
            for Point in Points:
                HostSummary = Summary.setdefault(Point.HostName, {})
                HostSummary[MetricName] = Point.Value
        return Summary, Errors

    def BuildAnomalies(self, Summary: dict[str, dict[str, float]], MetricErrors: list[str]) -> list[Anomaly]:
        Anomalies: list[Anomaly] = []
        if MetricErrors:
            Anomalies.append(
                Anomaly(
                    "Plataforma",
                    "Evidencia",
                    "Unknown",
                    "No se pudo consultar una o mas series de VictoriaMetrics.",
                    "Validar VictoriaMetrics, red interna y ejecucion de Scripts/UpdatePlatformZabbixStatus.sh.",
                )
            )
        if not Summary:
            Anomalies.append(
                Anomaly(
                    "Plataforma",
                    "Evidencia",
                    "Unknown",
                    "No hay metricas disponibles para el periodo consultado.",
                    "Generar datos con Scripts/UpdatePlatformZabbixStatus.sh o instalar el cron administrado.",
                )
            )
            return Anomalies

        for HostName, Values in sorted(Summary.items()):
            self.AppendThresholdAnomaly(Anomalies, HostName, "CPU", Values.get("CPU p95"), Values.get("CPU pico"))
            self.AppendThresholdAnomaly(Anomalies, HostName, "RAM", Values.get("RAM p95"), Values.get("RAM pico"))
            Availability = Values.get("Disponibilidad minima")
            if Availability is not None and Availability < 1:
                Anomalies.append(
                    Anomaly(
                        HostName,
                        "Disponibilidad",
                        "Critical",
                        f"El contenedor tuvo valor platform_container_up={Availability:.0f} en el periodo.",
                        "Revisar reinicios, logs del contenedor y causas de parada.",
                    )
                )
        if not Anomalies:
            Anomalies.append(
                Anomaly(
                    "Plataforma",
                    "Observacion",
                    "OK",
                    "No se detectaron umbrales criticos con la evidencia disponible.",
                    "Mantener captura continua para mejorar confianza de tendencia.",
                )
            )
        return Anomalies

    def AppendThresholdAnomaly(self, Anomalies: list[Anomaly], HostName: str, Metric: str, P95: float | None, Peak: float | None) -> None:
        if P95 is None and Peak is None:
            return
        P95Value = P95 if P95 is not None and math.isfinite(P95) else 0.0
        PeakValue = Peak if Peak is not None and math.isfinite(Peak) else 0.0
        if P95Value >= 85 or PeakValue >= 95:
            Severity = "Critical"
        elif P95Value >= 75 or PeakValue >= 90:
            Severity = "Warning"
        else:
            return
        Suggestion = "Analizar procesos, limites del contenedor y necesidad de escalamiento."
        if Metric == "RAM":
            Suggestion = "Revisar memoria retenida, cache, heap y limites del contenedor."
        Anomalies.append(
            Anomaly(
                HostName,
                Metric,
                Severity,
                f"{Metric} p95={P95Value:.2f}% pico={PeakValue:.2f}%",
                Suggestion,
            )
        )

    def CollectPostgreSqlRecommendations(self, LoadId: str) -> tuple[list[list[str]], list[str]]:
        Sql = f"""
select HostName, Priority, Action, Reason, Status
from (
  select coalesce(mr.Name, rec.ScopeId) as HostName, rec.Priority, rec.Action, rec.Reason, rec.Status
  from Recommendation rec
  left join MonitoredResource mr on mr.ResourceId = rec.ScopeId
  where rec.RecommendationId ~ '^{self.EscapeSqlLiteral(LoadId)}'
  union all
  select coalesce(c.ComponentName, rec.RiskId) as HostName, rec.Priority, rec.Action, rec.Rationale as Reason, rec.Status
  from EnterpriseRecommendation rec
  left join EnterpriseRiskRegistryEntry r on r.RiskId = rec.RiskId
  left join EnterpriseTechnologyComponent c on c.LoadId = rec.LoadId and c.ComponentId = any(string_to_array(r.AffectedTechnologyIds, ','))
  where rec.LoadId ~ '^{self.EscapeSqlLiteral(LoadId)}'
) Datos
order by case Priority when 'Critical' then 4 when 'High' then 3 when 'Medium' then 2 else 1 end desc, HostName
limit 20;
"""
        try:
            Output = self.PostgreSql.ExecuteSqlQuery(Sql)
        except Exception as Error:  # pragma: no cover - exercised against live stack
            return [], [str(Error)]
        Rows = []
        for Line in Output.splitlines():
            if not Line.strip():
                continue
            Rows.append([Column.strip() for Column in Line.split("|")])
        return Rows, []

    def EscapeSqlLiteral(self, Value: str) -> str:
        return Value.replace("'", "''")

    def BuildExecutiveSummary(self, Anomalies: list[Anomaly], MetricErrors: list[str], PostgreSqlErrors: list[str]) -> str:
        Critical = sum(1 for Item in Anomalies if Item.Severity == "Critical")
        Warning = sum(1 for Item in Anomalies if Item.Severity == "Warning")
        Unknown = sum(1 for Item in Anomalies if Item.Severity == "Unknown") + len(MetricErrors) + len(PostgreSqlErrors)
        if Critical:
            State = "CRITICAL"
        elif Warning:
            State = "WARNING"
        elif Unknown:
            State = "UNKNOWN"
        else:
            State = "OK"
        return f"Estado mensual: **{State}**. Criticas: {Critical}. Warning: {Warning}. Evidencia desconocida: {Unknown}."

    def BuildAnomalyTable(self, Anomalies: list[Anomaly]) -> str:
        Lines = ["| Host/Subsistema | Categoria | Severidad | Evidencia | Sugerencia |", "| --- | --- | --- | --- | --- |"]
        for Item in Anomalies:
            Lines.append(f"| {Item.HostName} | {Item.Category} | {Item.Severity} | {Item.Evidence} | {Item.Suggestion} |")
        return "\n".join(Lines)

    def BuildSuggestionList(self, Anomalies: list[Anomaly]) -> str:
        Actionable = [Item for Item in Anomalies if Item.Severity in {"Critical", "Warning", "Unknown"}]
        if not Actionable:
            return "- No hay acciones prioritarias con la evidencia disponible."
        return "\n".join(f"- **{Item.Severity} - {Item.HostName}:** {Item.Suggestion}" for Item in Actionable[:10])

    def BuildMetricTable(self, Summary: dict[str, dict[str, float]]) -> str:
        if not Summary:
            return "Sin datos de metricas para el periodo."
        Columns = ["CPU promedio", "CPU p95", "CPU pico", "RAM promedio", "RAM p95", "RAM pico", "Network pico", "IOPS pico", "Disponibilidad minima"]
        Lines = ["| Host | " + " | ".join(Columns) + " |", "| --- | " + " | ".join("---" for _ in Columns) + " |"]
        for HostName, Values in sorted(Summary.items()):
            Row = [self.FormatNumber(Values.get(Column)) for Column in Columns]
            Lines.append(f"| {HostName} | " + " | ".join(Row) + " |")
        return "\n".join(Lines)

    def BuildPostgreSqlTable(self, Rows: list[list[str]], Errors: list[str]) -> str:
        if Errors:
            return "No se pudieron consultar recomendaciones PostgreSQL:\n" + "\n".join(f"- {Error}" for Error in Errors)
        if not Rows:
            return "Sin recomendaciones registradas en PostgreSQL para el alcance consultado."
        Lines = ["| Host/Subsistema | Prioridad | Accion | Razon | Estado |", "| --- | --- | --- | --- | --- |"]
        for Row in Rows:
            SafeRow = (Row + ["", "", "", "", ""])[:5]
            Lines.append("| " + " | ".join(SafeRow) + " |")
        return "\n".join(Lines)

    def BuildEvidenceQuality(self, Summary: dict[str, dict[str, float]], MetricErrors: list[str], PostgreSqlErrors: list[str]) -> str:
        Lines = [
            f"- Hosts con evidencia VictoriaMetrics: {len(Summary)}",
            f"- Errores de consulta VictoriaMetrics: {len(MetricErrors)}",
            f"- Errores de consulta PostgreSQL: {len(PostgreSqlErrors)}",
        ]
        if MetricErrors:
            Lines.extend(f"- VictoriaMetrics: {Error}" for Error in MetricErrors[:5])
        if PostgreSqlErrors:
            Lines.extend(f"- PostgreSQL: {Error}" for Error in PostgreSqlErrors[:5])
        return "\n".join(Lines)

    def FormatNumber(self, Value: float | None) -> str:
        if Value is None:
            return "Sin datos"
        return f"{Value:.2f}"


def DefaultMonth() -> str:
    return datetime.now().strftime("%Y-%m")


def DefaultOutputPath(Month: str) -> Path:
    return Path("Reports") / "Operational" / f"ReporteOperativoMensual-{Month}.md"


def Main() -> int:
    Parser = argparse.ArgumentParser(description="Genera reporte operativo mensual con anomalias y sugerencias.")
    Parser.add_argument("--month", default=DefaultMonth(), help="Mes a reportar en formato YYYY-MM.")
    Parser.add_argument("--load-id", default="Infraestructura", help="Lote o alcance VictoriaMetrics/PostgreSQL.")
    Parser.add_argument("--output", default=None, help="Ruta del reporte Markdown de salida.")
    Args = Parser.parse_args()

    OutputPath = Path(Args.output) if Args.output else DefaultOutputPath(Args.month)
    Report = MonthlyOperationalReport()
    PathValue = Report.Build(Args.month, Args.load_id, OutputPath)
    print(f"INFO: reporte operativo mensual generado: {PathValue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(Main())
