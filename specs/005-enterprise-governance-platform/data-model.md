# Data Model: Enterprise Governance Platform

## TechnologyDomain

Represents a supported enterprise technology domain.

**Fields**:

- `DomainId`: stable identifier.
- `Name`: Infrastructure, OperatingSystem, Database, Middleware, ContainerPlatform,
  MessagingPlatform, MonitoringPlatform, EnterpriseApplication, or BusinessService.
- `Description`: business-readable description.
- `Status`: Active, Deprecated, or Disabled.

**Validation Rules**:

- `Name` is required and unique.
- Disabled domains cannot receive new inventory records.

## TechnologyComponent

Represents a monitored or governed technology element.

**Fields**:

- `ComponentId`: stable identifier.
- `ComponentName`: visible name.
- `TechnologyType`: server, virtual machine, database, middleware, application, service, or other
  controlled value.
- `DomainId`: associated TechnologyDomain.
- `Version`: technology version where available.
- `Vendor`: vendor or provider.
- `Environment`: Production, NonProduction, Development, Test, or Unknown.
- `BusinessServiceId`: optional associated business service.
- `Owner`: accountable owner or team.
- `SupportStatus`: Supported, Backlevel, EndOfSupport, EndOfLife, or Unknown.
- `LifecycleStatus`: Current, AttentionRequired, AtRisk, Critical, or Unknown.
- `EvidenceState`: Available, Missing, Unknown, Incomplete, or Unverified.

**Relationships**:

- Belongs to one TechnologyDomain.
- May support one or more BusinessServices through ServiceComponentMap.
- Has many EvidenceRecords, RiskAssessments, and ScoreAssessments.

**Validation Rules**:

- `ComponentName`, `TechnologyType`, `DomainId`, and `EvidenceState` are required.
- Missing lifecycle evidence must produce `SupportStatus = Unknown` or `LifecycleStatus = Unknown`.

## BusinessService

Represents a business-facing service or application grouping.

**Fields**:

- `BusinessServiceId`: stable identifier.
- `ServiceName`: visible service name.
- `ServiceOwner`: accountable owner or team.
- `Criticality`: Low, Medium, High, or Critical.
- `Status`: Active, Degraded, Critical, Retired, or Unknown.

**Relationships**:

- Has many TechnologyComponents through ServiceComponentMap.
- Has many RiskRegistryEntries through affected service mappings.

## ServiceComponentMap

Maps technology components to business services.

**Fields**:

- `MapId`: stable identifier.
- `BusinessServiceId`: service reference.
- `ComponentId`: component reference.
- `Role`: Application, Database, Middleware, Storage, Network, Monitoring, or Other.
- `ImpactWeight`: numeric contribution to service risk.

**Validation Rules**:

- `ImpactWeight` must be 0-100.
- A component shared by multiple services must remain visible in every affected service context.

## EvidenceRecord

Represents evidence used by assessments.

**Fields**:

- `EvidenceId`: stable identifier.
- `SourceSystem`: Zabbix, VictoriaMetrics, PostgreSQL, ManualRecord, SyntheticDataset, or Other.
- `EvidenceType`: Telemetry, Inventory, Availability, Event, Lifecycle, Compliance, Trend, or
  Forecast.
- `ComponentId`: optional component reference.
- `BusinessServiceId`: optional service reference.
- `ObservedAt`: timestamp of evidence.
- `FreshnessStatus`: Fresh, Stale, Expired, or Unknown.
- `EvidenceState`: Available, Missing, Unknown, Incomplete, or Unverified.
- `EvidenceReference`: source query, record id, metric label, dashboard reference, or file path.

**Validation Rules**:

- Every assessment must reference at least one EvidenceRecord or an explicit missing evidence state.
- Stale or incomplete evidence must reduce MonitoringConfidenceScore.

## AssessmentRun

Represents one execution of enterprise assessment calculations.

**Fields**:

- `AssessmentRunId`: stable identifier.
- `StartedAt`: run start timestamp.
- `CompletedAt`: optional completion timestamp.
- `Status`: Running, Succeeded, Failed, or Partial.
- `Scope`: domain, component, service, or enterprise scope.
- `EvidenceWindowStart`: start of evidence window.
- `EvidenceWindowEnd`: end of evidence window.

## ScoreAssessment

Represents a 0-100 score for an assessment area.

**Fields**:

- `ScoreAssessmentId`: stable identifier.
- `AssessmentRunId`: run reference.
- `ScoreType`: Capacity, Performance, Availability, Lifecycle, Compliance, MonitoringConfidence,
  or TechnologyHealth.
- `ScopeType`: Enterprise, Domain, BusinessService, or TechnologyComponent.
- `ScopeId`: referenced scope identifier.
- `ScoreValue`: 0-100.
- `Classification`: Excellent, Healthy, AttentionRequired, AtRisk, or Critical.
- `EvidenceState`: Available, Missing, Unknown, Incomplete, or Unverified.
- `CalculatedAt`: timestamp.

**Validation Rules**:

- `ScoreValue` must be between 0 and 100.
- TechnologyHealth classification must follow the 90/75/60/40 thresholds.
- Missing evidence cannot produce Excellent or Healthy classification.

## RiskAssessment

Represents a domain-specific risk calculated from evidence.

**Fields**:

- `RiskAssessmentId`: stable identifier.
- `AssessmentRunId`: run reference.
- `RiskCategory`: Capacity, Performance, Availability, Lifecycle, Compliance, or Monitoring.
- `Severity`: Low, Medium, High, or Critical.
- `Impact`: business-readable impact.
- `ScopeType`: Enterprise, Domain, BusinessService, or TechnologyComponent.
- `ScopeId`: referenced scope identifier.
- `EvidenceState`: Available, Missing, Unknown, Incomplete, or Unverified.
- `Reason`: explanation.
- `CalculatedAt`: timestamp.

**Validation Rules**:

- Each risk must identify affected technologies and services through RiskRegistryEntry mappings.
- Risks must be reproducible from referenced evidence.

## RiskRegistryEntry

Represents the shared risk object for governance and executive decisions.

**Fields**:

- `RiskId`: stable risk identifier.
- `RiskAssessmentId`: assessment reference.
- `RiskCategory`: Capacity, Performance, Availability, Lifecycle, Compliance, or Monitoring.
- `Severity`: Low, Medium, High, or Critical.
- `Impact`: business-readable impact.
- `AffectedTechnologyIds`: one or more TechnologyComponent references.
- `AffectedServiceIds`: zero or more BusinessService references.
- `RecommendedAction`: action proposal.
- `Status`: Open, Accepted, Mitigating, Closed, or Deferred.
- `Owner`: accountable owner or team.
- `EvidenceState`: Available, Missing, Unknown, Incomplete, or Unverified.

**Validation Rules**:

- Every open risk must include severity, impact, affected technologies, and recommended action.
- If no service mapping exists, the risk must show the mapping gap instead of hiding the component.

## Recommendation

Represents a decision-support recommendation.

**Fields**:

- `RecommendationId`: stable identifier.
- `RiskId`: risk reference.
- `Priority`: Low, Medium, High, or Critical.
- `Action`: recommended action.
- `Rationale`: evidence-backed rationale.
- `DecisionOwner`: authorized decision owner or team.
- `Status`: Open, Accepted, Rejected, Completed, or Deferred.

**Validation Rules**:

- Recommendations must not execute remediation automatically.
- Recommendations must reference evidence and affected technologies/services through the risk.

## ForecastResult

Represents a forecast derived from historical evidence.

**Fields**:

- `ForecastId`: stable identifier.
- `AssessmentRunId`: run reference.
- `ComponentId`: component reference.
- `MetricName`: CPU, Memory, Storage, Filesystem, or other controlled value.
- `Forecast30Days`: optional projected value.
- `Forecast90Days`: optional projected value.
- `Forecast180Days`: optional projected value.
- `Forecast365Days`: optional projected value.
- `DaysToExhaustion`: optional days to saturation or exhaustion.
- `EvidenceState`: Available, Missing, Unknown, Incomplete, or Unverified.
- `Confidence`: Low, Medium, or High.

**Validation Rules**:

- Forecast horizons without sufficient history must remain empty and report insufficient evidence.
- Forecast outputs must identify source evidence window and component.

## State Transitions

### RiskRegistryEntry.Status

```text
Open -> Accepted -> Mitigating -> Closed
Open -> Deferred
Open -> Closed
Open -> Rejected
Deferred -> Accepted
Mitigating -> Deferred
```

### EvidenceState

```text
Unknown -> Available
Unknown -> Missing
Available -> Incomplete
Available -> Unverified
Incomplete -> Available
Unverified -> Available
Available -> Missing
```
