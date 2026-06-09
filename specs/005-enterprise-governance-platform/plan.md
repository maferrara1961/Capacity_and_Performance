# Implementation Plan: Enterprise Governance Platform

**Branch**: `main` | **Date**: 2026-06-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/005-enterprise-governance-platform/spec.md`

## Summary

Extend Capacity_and_Performance from a capacity/performance observability stack into an enterprise
technology governance platform. The implementation will add domain models and evidence-backed
assessment flows for technology inventory, capacity, performance, availability, lifecycle,
compliance, monitoring confidence, risk registry, scoring, and executive/operational dashboards.

The technical approach preserves the current Podman stack and Clean Architecture structure:
domain policy and scoring live in `CapacityEngine/Domain` and `CapacityEngine/Application`,
source-system access remains in adapters, reporting datasets stay in PostgreSQL, time-series
evidence remains in VictoriaMetrics, inventory and monitoring evidence remains governed by Zabbix,
and Grafana remains the visualization layer.

## Technical Context

**Language/Version**: Python 3.11 for CapacityEngine runtime; shell scripts for stack
administration; JSON/YAML provisioning for Grafana and Podman.

**Primary Dependencies**: Existing runtime/platform APIs only. No new external Python libraries,
SDKs, packages, hosted services, or proprietary licensed components.

**Storage**: PostgreSQL `capacity` database for inventory, lifecycle, compliance, risk, scoring,
and reporting datasets; VictoriaMetrics for historical metric evidence; Zabbix/PostgreSQL for
monitoring and inventory evidence; Grafana SQLite only for Grafana internal state.

**Testing**: Existing stdlib `unittest` suite executed through `Scripts/RunTests.sh`, with unit,
contract, and integration tests under `Tests/`.

**Target Platform**: Linux/Podman self-hosted stack, validated locally and on remote Ubuntu hosts.

**Project Type**: Self-hosted observability/governance platform with Python batch engine, shell
administration scripts, Grafana dashboards, and containerized services.

**Performance Goals**: Support 10,000+ monitored components, multi-year historical retention, and
executive state comprehension within sixty seconds.

**Constraints**: No healthy inference from missing evidence; all scores must be 0-100 and
traceable; protected dashboards/commands require authentication; user-controlled inputs must be
validated; project-defined symbols use PascalCase unless external platform conventions require an
exception.

**Scale/Scope**: Enterprise technology domains covering infrastructure, operating systems,
databases, middleware, container platforms, messaging platforms, monitoring platforms, enterprise
applications, and business services.

**Technology Domains Affected**: Capacity, Performance, Availability, Lifecycle, Compliance, and
Monitoring Governance.

**Evidence Sources**: Zabbix monitoring/inventory/events, VictoriaMetrics historical metrics,
PostgreSQL metadata/inventory/lifecycle/compliance/risk datasets, Grafana dashboard presentation,
and generated validation datasets.

**Assessment Outputs**: Capacity Risk Assessment, Performance Risk Assessment, Availability Risk
Assessment, Lifecycle Risk Assessment, Compliance Risk Assessment, Monitoring Confidence
Assessment, Technology Health Score, risk registry entries, and executive/operational dashboards.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **TDD**: PASS. Plan requires failing unit/contract/integration tests for evidence states,
  scoring, risk registry, protected access, and dashboard data contracts before implementation.
- **SOLID / Clean Architecture**: PASS. Domain models and scoring policy stay independent from
  Zabbix, VictoriaMetrics, PostgreSQL, Grafana, shell, and Podman adapters.
- **DRY / YAGNI**: PASS. Reuse existing `CapacityEngine` layers, synthetic data mechanisms, and
  dashboard provisioning; avoid speculative integrations beyond the declared enterprise domains.
- **PascalCase**: PASS. New project-defined Python symbols, table-like entity names, and artifact
  names use PascalCase; external metric labels and Grafana JSON conventions remain documented
  exceptions.
- **No New External Libraries**: PASS. Implementation uses stdlib Python, existing shell tooling,
  existing Podman images, and approved platform APIs only.
- **Validation and Auth**: PASS. User-controlled script inputs, dashboard filters, governance
  updates, inventory changes, and risk registry commands must be validated; Grafana and Zabbix
  views remain authenticated.
- **Platform Scope**: PASS. The model represents domain and technology type as data so future
  technologies can be added without redesigning assessment policy.
- **Evidence Handling**: PASS. Evidence states include available, missing, unknown, incomplete,
  and unverified, and missing evidence cannot produce healthy status.
- **Risk and Trend Logic**: PASS. Risk and scoring criteria are objective, reproducible, and
  traceable; forecasts require historical evidence and must show insufficient-evidence states.
- **Scoring**: PASS. All domain scores and Technology Health Score use a 0-100 range with
  classification thresholds from the specification.
- **Human Decision Support**: PASS. Recommendations identify affected technologies/services and
  support human decisions without automated remediation.

## Project Structure

### Documentation (this feature)

```text
specs/005-enterprise-governance-platform/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── cli-contract.md
│   ├── dashboard-contract.md
│   └── dataset-contract.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
CapacityEngine/
├── Domain/              # Enterprise inventory, evidence, score, risk, and recommendation policy
├── Application/         # Assessment, scoring, orchestration, validation, and use cases
├── Adapters/            # PostgreSQL, VictoriaMetrics, Zabbix, and command adapters
└── Scheduler/           # Batch entry points and CLI commands

Config/
├── Grafana/
│   ├── Dashboards/      # Executive, operational, planning, application, and governance views
│   ├── Datasources/
│   └── DashboardProviders/
├── PodmanStack.yml
└── StackManifest.yml

Scripts/                 # Build/start/stop/status/logs/sync/load/validate commands
Tests/
├── Unit/
├── Contract/
└── Integration/
docs/
```

**Structure Decision**: Use the existing single-repository platform layout. Domain expansion will
be implemented inside `CapacityEngine` and existing configuration/script folders so governance
features share the same stack, validation, and deployment model as the current capacity platform.

## Complexity Tracking

No constitution violations are planned.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
