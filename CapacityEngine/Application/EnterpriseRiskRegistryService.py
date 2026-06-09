from CapacityEngine.Domain.EnterpriseEntities import RiskAssessment, RiskRegistryEntry


class EnterpriseRiskRegistryService:
    def BuildEntry(self, Risk: RiskAssessment, TechnologyIds: tuple[str, ...], ServiceIds: tuple[str, ...] = ()) -> RiskRegistryEntry:
        return RiskRegistryEntry(
            RiskId=f"{Risk.RiskAssessmentId}-Registry",
            RiskAssessmentId=Risk.RiskAssessmentId,
            RiskCategory=Risk.RiskCategory,
            Severity=Risk.Severity,
            Impact=Risk.Impact,
            AffectedTechnologyIds=TechnologyIds,
            AffectedServiceIds=ServiceIds,
            RecommendedAction=f"Revisar {Risk.RiskCategory.value} y planificar mitigacion",
            Owner="CapacityLab",
            EvidenceState=Risk.EvidenceState,
        )

    def TopRisks(self, Entries: list[RiskRegistryEntry], Limit: int = 10) -> list[RiskRegistryEntry]:
        Weight = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        return sorted(Entries, key=lambda Entry: Weight.get(Entry.Severity.value, 0), reverse=True)[:Limit]
