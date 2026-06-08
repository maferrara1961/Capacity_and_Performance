from pathlib import Path


class PostgreSqlCommandAdapter:
    def __init__(self, SqlRoot: str = "Sql") -> None:
        self.SqlRoot = Path(SqlRoot)

    def ReadSql(self, RelativePath: str) -> str:
        return (self.SqlRoot / RelativePath).read_text(encoding="utf-8")

    def BuildPsqlCommand(self, DatabaseUrl: str, RelativePath: str) -> list[str]:
        return ["psql", DatabaseUrl, "-f", str(self.SqlRoot / RelativePath)]

    def SaveKpis(self, Kpis: list[object]) -> None:
        self.LastSavedKpis = list(Kpis)

    def SaveForecasts(self, Forecasts: list[object]) -> None:
        self.LastSavedForecasts = list(Forecasts)

    def SaveRisks(self, Risks: list[object]) -> None:
        self.LastSavedRisks = list(Risks)

    def SaveRecommendations(self, Recommendations: list[object]) -> None:
        self.LastSavedRecommendations = list(Recommendations)
