# Dataset Contract: Enterprise Governance Platform

## Purpose

Enterprise governance datasets must be consistent across PostgreSQL, VictoriaMetrics, Zabbix, and
Grafana so stakeholders see the same technologies, services, evidence, risks, scores, and
recommendations.

## Required Dataset Groups

### Inventory

- TechnologyDomain.
- TechnologyComponent.
- BusinessService.
- ServiceComponentMap.

### Evidence

- TelemetryEvidence.
- LifecycleEvidence.
- ComplianceEvidence.
- AvailabilityEvidence.
- MonitoringCoverageEvidence.
- EvidenceState.

### Assessment

- AssessmentRun.
- ScoreAssessment.
- RiskAssessment.
- ForecastResult.
- RiskRegistryEntry.
- Recommendation.

## Identity Consistency

- Component visible name must be stable across Zabbix, PostgreSQL, VictoriaMetrics labels, and
  Grafana panels.
- Internal identifiers may exist for joins and cleanup, but executive dashboards must show
  business-readable names.
- Business service references must be shared by score, risk, and recommendation outputs.

## Evidence State Rules

- Available evidence can support healthy status only when risk criteria pass.
- Missing evidence cannot support healthy, compliant, or supported status.
- Unknown evidence must remain visible in dashboard and registry outputs.
- Incomplete evidence must reduce Monitoring Confidence Score.
- Unverified evidence must require review before supporting final conclusions.

## Score Rules

- All scores are integers or decimals in the range 0-100.
- Technology Health Score classification uses the required thresholds:
  - 90-100: Excellent.
  - 75-89: Healthy.
  - 60-74: Attention Required.
  - 40-59: At Risk.
  - 0-39: Critical.

## Forecast Rules

- Forecasts must include 30 and 90 days when sufficient evidence exists.
- Forecasts should include 180 and 365 days when sufficient history exists.
- Insufficient history must produce an explicit evidence limitation.

## Deletion Rules

- Generated verification datasets must be deletable by load id.
- Delete-all mode must require explicit confirmation.
- Deletion must not remove non-generated operational inventory or manually managed evidence.
