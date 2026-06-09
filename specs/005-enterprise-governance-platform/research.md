# Research: Enterprise Governance Platform

## Decision: Keep the Existing Approved Toolchain

Capacity_and_Performance will continue to use Zabbix, VictoriaMetrics, PostgreSQL, Grafana,
Podman, shell scripts, and Python stdlib only.

**Rationale**: The constitution prohibits new external libraries and the project already has a
working stack, validation scripts, synthetic data loader, and dashboard provisioning model.

**Alternatives considered**:

- Add a new analytics engine: rejected because it introduces dependency and licensing risk.
- Add a new workflow/orchestration platform: rejected because current batch scripts and
  CapacityEngine are sufficient for planned assessments.

## Decision: Model Technology Domains as Data

Technology domains, component types, business services, lifecycle states, compliance states, and
evidence states will be modeled as data attributes rather than hard-coded per-domain classes.

**Rationale**: The platform must support infrastructure, OS, database, middleware, container,
messaging, monitoring, enterprise application, and future domains without redesigning the platform.

**Alternatives considered**:

- Separate code paths for each technology domain: rejected due to duplication and poor
  extensibility.
- Free-form text only: rejected because scoring, filtering, and auditability require controlled
  values and validation.

## Decision: Treat Missing Evidence as a First-Class State

Evidence status will explicitly include Available, Missing, Unknown, Incomplete, and Unverified.
Missing or weak evidence reduces monitoring confidence and must not be interpreted as healthy.

**Rationale**: The constitution and specification both prohibit inferring healthy status from
missing data.

**Alternatives considered**:

- Null values only: rejected because null does not explain whether evidence is missing, unknown,
  incomplete, or unverified.
- Exclude incomplete records: rejected because hiding gaps creates false confidence.

## Decision: Score Everything on a 0-100 Scale

Capacity, Performance, Availability, Lifecycle, Compliance, Monitoring Confidence, and Technology
Health scores will use a normalized 0-100 scale. Technology Health classification follows:
Excellent 90-100, Healthy 75-89, Attention Required 60-74, At Risk 40-59, Critical 0-39.

**Rationale**: A common score range supports executive comparison and reproducible reporting.

**Alternatives considered**:

- Domain-specific score ranges: rejected because they complicate executive interpretation.
- Status-only output: rejected because stakeholders need trending and prioritization.

## Decision: Risk Registry Is the Shared Decision Object

Every risk entry will identify category, severity, impact, affected technologies, affected
services, evidence state, evidence references, and recommended action.

**Rationale**: This gives executives, governance users, and operations teams one shared language
for decision support.

**Alternatives considered**:

- Dashboard-only risk rendering: rejected because risk decisions need auditability and reuse.
- Tool-specific alerts only: rejected because raw alerts do not carry lifecycle, compliance, and
  business service context.

## Decision: Historical Evidence Is Required for Forecasts

Forecasts for 30, 90, 180, and 365 days require sufficient historical evidence. If evidence is
insufficient, the forecast output must show an insufficient-evidence state instead of fabricating a
projection.

**Rationale**: Trend principles prioritize historical behavior over snapshots and require
traceability.

**Alternatives considered**:

- Always forecast from latest point: rejected because it creates unsupported conclusions.
- Hide forecasts when insufficient: rejected because stakeholders must see evidence gaps.

## Decision: Contracts Cover CLI, Dataset, and Dashboard Behavior

This feature exposes operational behavior through scripts, generated datasets, and Grafana
dashboards, so contracts are documented as command, dataset, and dashboard expectations.

**Rationale**: The project is not a public web API. The relevant external surfaces are commands,
data artifacts, and dashboards.

**Alternatives considered**:

- OpenAPI contracts: rejected because no HTTP API is defined for this feature.
- No contracts: rejected because Spec Kit planning requires testable interface expectations.
