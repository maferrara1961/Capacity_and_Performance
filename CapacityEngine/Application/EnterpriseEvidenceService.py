from datetime import datetime, timedelta

from CapacityEngine.Domain.EnterpriseConstants import EvidenceState, FreshnessStatus


class EnterpriseEvidenceService:
    def FreshnessStatus(self, ObservedAt: datetime | None, Now: datetime) -> FreshnessStatus:
        if ObservedAt is None:
            return FreshnessStatus.UNKNOWN
        Age = Now - ObservedAt
        if Age <= timedelta(days=1):
            return FreshnessStatus.FRESH
        if Age <= timedelta(days=7):
            return FreshnessStatus.STALE
        return FreshnessStatus.EXPIRED

    def MonitoringConfidence(self, EvidenceStates: list[EvidenceState]) -> float:
        if not EvidenceStates:
            return 0.0
        Penalties = {
            EvidenceState.AVAILABLE: 0,
            EvidenceState.UNVERIFIED: 15,
            EvidenceState.INCOMPLETE: 25,
            EvidenceState.UNKNOWN: 35,
            EvidenceState.MISSING: 60,
        }
        TotalPenalty = sum(Penalties[State] for State in EvidenceStates)
        return max(0.0, round(100 - (TotalPenalty / len(EvidenceStates)), 2))
