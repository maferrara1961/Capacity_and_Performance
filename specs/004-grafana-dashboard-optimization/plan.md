# Implementation Plan: Grafana Dashboard Optimization

**Branch**: `004-grafana-dashboard-optimization` | **Date**: 2026-06-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-grafana-dashboard-optimization/spec.md`

## Summary

Optimize the capacity and performance dashboards into two clearly separated dashboard families:
executive views for decision making and technical views for operational improvement. The delivery
will refine Grafana dashboard JSON, preserve existing PostgreSQL and VictoriaMetrics data sources,
extend validation coverage, and use existing synthetic verification scenarios to prove that normal,
warning, critical, and mixed states populate the dashboard set.

## Technical Context

**Language/Version**: Python 3.11-compatible standard library for validation and synthetic data tooling; Bash for stack scripts; JSON/YAML dashboard provisioning artifacts.

**Primary Dependencies**: Existing runtime/platform APIs only: Python standard library, Podman CLI, Grafana OSS provisioning, PostgreSQL container, VictoriaMetrics container, and existing project scripts. No new external libraries, SDKs, packages, or hosted services.

**Storage**: PostgreSQL stores catalog, capacity KPI, forecast, risk, recommendation, and test-load metadata. VictoriaMetrics stores performance time series. Grafana stores its own operational state in the existing persistent volume while reading provisioned dashboard and datasource definitions from the repository.

**Testing**: Existing `Scripts/RunTests.sh` using Python `unittest`, plus `Scripts/ValidateStack.sh`, dry-run stack validation, and synthetic data validation commands.

**Target Platform**: Linux server running Podman containers, with local and public-access validation through existing stack scripts.

**Project Type**: Self-hosted observability stack with CLI administration scripts, dashboard provisioning files, and a Python capacity engine.

**Performance Goals**: Executive users identify top 5 capacity risks and next actions in under 2 minutes; technical users identify affected service, resource, metric, and severity in under 3 minutes; dashboards remain readable with small, medium, and large synthetic datasets.

**Constraints**: No external libraries or licensed services; protected dashboard and data-generation surfaces must rely on existing authentication/operator access; project-defined symbols stay PascalCase except external schema conventions; implementation must remain narrowly scoped to dashboard optimization and validation support.

**Scale/Scope**: Four provisioned dashboard categories, existing verification profiles (`normal`, `warning`, `critical`, `mixed`), current service/resource/KPI/forecast/risk/recommendation data contracts, and existing stack lifecycle scripts.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **TDD**: PASS. Plan includes contract tests for dashboard purpose, required panels, datasource binding, KPI coverage, empty-state behavior, and synthetic scenario validation before implementation changes.
- **SOLID / Clean Architecture**: PASS. Dashboard JSON remains presentation/infrastructure. Capacity and performance concepts are represented through existing domain/application data contracts. Domain logic is not coupled to Grafana schema.
- **DRY / YAGNI**: PASS. The plan reuses existing dashboards, synthetic profiles, stack scripts, and validation commands. No speculative dashboard framework or new abstraction is introduced.
- **PascalCase**: PASS. Project-defined Python symbols and scripts keep existing PascalCase convention. Grafana JSON/YAML field names remain documented external schema exceptions.
- **No New External Libraries**: PASS. No packages, SDKs, hosted services, or licensed components are added.
- **Validation and Auth**: PASS. User-controlled inputs are time range, service/resource selectors, load identifiers, profile names, and volume options. Existing validation and Grafana/Zabbix authentication/operator access remain required for protected surfaces.

## Project Structure

### Documentation (this feature)

```text
specs/004-grafana-dashboard-optimization/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── DashboardCatalogContract.md
│   └── VerificationScenarioContract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
Config/
└── Grafana/
    ├── DashboardProviders/
    │   └── Provisioning.yml
    ├── Dashboards/
    │   ├── ApplicationDashboard.json
    │   ├── CapacityPlanningDashboard.json
    │   ├── ExecutiveCapacityDashboard.json
    │   └── TechnicalPerformanceDashboard.json
    └── Datasources/
        └── Datasources.yml

CapacityEngine/
├── Application/
│   └── SyntheticDataService.py
├── Adapters/
│   ├── SyntheticPostgreSqlAdapter.py
│   └── SyntheticVictoriaMetricsAdapter.py
└── Scheduler/
    └── SyntheticDataCommand.py

Scripts/
├── GenerateVerificationBatches.sh
├── ManageTestData.sh
├── StartStack.sh
├── StackCommon.sh
├── StackStatus.sh
└── ValidateStack.sh

Tests/
├── Contract/
│   ├── ApplicationDashboardContractTest.py
│   ├── CapacityPlanningDashboardContractTest.py
│   ├── ExecutiveDashboardContractTest.py
│   ├── GrafanaDatasourceContractTest.py
│   ├── StackInterconnectionContractTest.py
│   └── TechnicalDashboardContractTest.py
└── Integration/
    ├── CapacityPlanningFlowTest.py
    ├── ExecutiveCapacityFlowTest.py
    ├── SyntheticDataFlowTest.py
    └── TechnicalPerformanceFlowTest.py
```

**Structure Decision**: Use the existing single-repository observability stack layout. Dashboard definitions stay under `Config/Grafana`; validation and synthetic data remain under `CapacityEngine`, `Scripts`, and `Tests`. No new application package is introduced.

## Complexity Tracking

No constitution violations require justification.

## Phase 0 Research Summary

Research decisions are documented in [research.md](research.md). All technical unknowns were resolved without requiring clarification from the user.

## Phase 1 Design Summary

Data model decisions are documented in [data-model.md](data-model.md). User-facing contracts are documented in [contracts/DashboardCatalogContract.md](contracts/DashboardCatalogContract.md) and [contracts/VerificationScenarioContract.md](contracts/VerificationScenarioContract.md). Validation steps are documented in [quickstart.md](quickstart.md).

## Post-Design Constitution Check

- **TDD**: PASS. Planned tasks will start with contract and integration tests for all three user stories before dashboard implementation.
- **SOLID / Clean Architecture**: PASS. No domain dependency on Grafana or provisioning schema is introduced.
- **DRY / YAGNI**: PASS. Existing dashboards and synthetic data commands are extended, not replaced by new systems.
- **PascalCase**: PASS. External dashboard schema keys remain exceptions; project-defined artifacts are named consistently.
- **No New External Libraries**: PASS. Design uses current stack and standard runtime only.
- **Validation and Auth**: PASS. Existing command validation and authenticated dashboard access remain part of the acceptance path.
