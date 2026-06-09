from CapacityEngine.Domain.EnterpriseConstants import EnterpriseRiskSeverity, EvidenceState, FreshnessStatus
from CapacityEngine.Domain.EnterpriseEntities import EvidenceRecord, TechnologyComponent


class EnterpriseGovernanceService:
    def MonitoringConfidence(self, EvidenceRecords: list[EvidenceRecord]) -> float:
        if not EvidenceRecords:
            return 0.0
        Penalty = 0
        for Evidence in EvidenceRecords:
            if Evidence.EvidenceState == EvidenceState.MISSING:
                Penalty += 50
            elif Evidence.EvidenceState in {EvidenceState.UNKNOWN, EvidenceState.INCOMPLETE}:
                Penalty += 25
            elif Evidence.EvidenceState == EvidenceState.UNVERIFIED:
                Penalty += 15
            if Evidence.FreshnessStatus == FreshnessStatus.EXPIRED:
                Penalty += 25
            elif Evidence.FreshnessStatus == FreshnessStatus.STALE:
                Penalty += 10
        return max(0.0, round(100 - (Penalty / len(EvidenceRecords)), 2))

    def LifecycleRisk(self, Component: TechnologyComponent) -> EnterpriseRiskSeverity:
        Status = Component.LifecycleStatus.lower()
        if Status in {"endoflife", "eol", "critical"}:
            return EnterpriseRiskSeverity.CRITICAL
        if Status in {"endofsupport", "deprecated", "atrisk"}:
            return EnterpriseRiskSeverity.HIGH
        if Status in {"unknown", "missing"}:
            return EnterpriseRiskSeverity.MEDIUM
        return EnterpriseRiskSeverity.LOW

    def ComplianceRisk(self, Component: TechnologyComponent) -> EnterpriseRiskSeverity:
        Status = Component.SupportStatus.lower()
        if Status in {"noncompliant", "unsupported"}:
            return EnterpriseRiskSeverity.CRITICAL
        if Status in {"unknown", "missing", "unverified"}:
            return EnterpriseRiskSeverity.MEDIUM
        return EnterpriseRiskSeverity.LOW
