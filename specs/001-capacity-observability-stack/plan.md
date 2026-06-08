# Implementation Plan: Capacity Observability Stack

**Branch**: `001-capacity-observability-stack` | **Date**: 2026-06-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-capacity-observability-stack/spec.md`

## Summary

Build a self-hosted, no-license-cost capacity observability stack using Podman images for Zabbix,
VictoriaMetrics, Grafana, PostgreSQL, and a daily Python capacity engine. The stack will collect
systems and subsystem metrics, map infrastructure to services, calculate capacity KPIs and
forecasts, and expose executive, technical, capacity planning, and application dashboard views.

The technical approach separates domain behavior from adapters: capacity calculations, risk scoring,
service catalog rules, and recommendations live in the domain/application layer; Podman image
definitions, scheduler commands, Grafana provisioning, monitoring collectors, and persistence are
adapters around that core.

## Technical Context

**Language/Version**: Python 3.11+ for the capacity engine using standard library only; shell for
container orchestration scripts; SQL for persistence definitions.

**Primary Dependencies**: Requested self-hosted platform components only: Podman, Zabbix,
VictoriaMetrics, Grafana, and PostgreSQL. No additional application-code libraries, SDKs, packages,
hosted services, or license-cost services are permitted.

**Storage**: PostgreSQL stores catalog, thresholds, baselines, KPI results, forecasts,
recommendations, and run history. VictoriaMetrics stores time-series metrics. Grafana reads from
provisioned data sources and dashboards.

**Testing**: Python standard-library `unittest`; shell smoke tests; SQL validation scripts;
dashboard provisioning validation via file and expected-query checks.

**Target Platform**: Linux host capable of running rootless or rootful Podman containers.

**Project Type**: Infrastructure stack plus scheduled capacity calculation engine and dashboard
provisioning.

**Performance Goals**: Daily capacity run completes before business hours for 99% of scheduled
runs; 95% of monitored services show refreshed risk state within 5 minutes after data refresh;
executive users identify top 10 saturation risks in under 2 minutes.

**Constraints**: No new external application-code libraries; no license-cost runtime services;
protected dashboards and catalog actions require authentication; all user-controlled inputs require
validation; project-defined symbols and artifacts use PascalCase except documented platform
conventions.

**Scale/Scope**: Initial version supports service catalog mapping, capacity KPIs, 30/60/90 day
forecasts, top consumers, visual alerts, and four dashboard families: executive, technical,
capacity planning, and application.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **TDD**: PASS. Tasks must create failing tests before implementation for capacity formulas,
  forecast windows, risk classification, catalog validation, protected access, and dashboard
  provisioning contracts.
- **SOLID / Clean Architecture**: PASS. Domain/application behavior is isolated from Podman,
  Grafana, Zabbix, VictoriaMetrics, PostgreSQL, and scheduler adapters.
- **DRY / YAGNI**: PASS. Initial scope implements required KPI and forecast behavior only; shared
  abstractions are limited to catalog, metric, threshold, forecast, and risk concepts used across
  multiple dashboards.
- **PascalCase**: PASS with documented exceptions. Project-defined symbols and artifacts use
  PascalCase where allowed. Platform-required names such as container image tags, SQL identifiers,
  metric names, and Grafana provisioning paths may use their required conventions.
- **No New External Libraries**: PASS. Requested platform components are accepted as feature
  constraints. Python code must use the standard library only; database access can be performed
  through approved platform command adapters or generated SQL files rather than application-code
  client packages.
- **Validation and Auth**: PASS. Catalog entries, thresholds, filters, baseline selections,
  forecast windows, scheduler inputs, and credentials are validation boundaries; dashboards and
  catalog/capacity results are protected.

## Project Structure

### Documentation (this feature)

```text
specs/001-capacity-observability-stack/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   |-- CapacityEngineContract.md
|   |-- DashboardContract.md
|   `-- ServiceCatalogContract.md
`-- tasks.md
```

### Source Code (repository root)

```text
ContainerImages/
|-- Zabbix/
|-- VictoriaMetrics/
|-- Grafana/
|-- PostgreSQL/
`-- CapacityEngine/

Config/
|-- Grafana/
|   |-- Dashboards/
|   `-- Datasources/
|-- Zabbix/
|-- VictoriaMetrics/
`-- PostgreSQL/

CapacityEngine/
|-- Domain/
|-- Application/
|-- Adapters/
|-- Scheduler/
`-- Tests/

Scripts/
|-- StartStack.sh
|-- StopStack.sh
|-- ValidateStack.sh
`-- RunCapacityDaily.sh

Sql/
|-- Schema/
|-- Seed/
`-- Validation/

Tests/
|-- Contract/
|-- Integration/
`-- Unit/
```

**Structure Decision**: Use an infrastructure-stack layout with PascalCase project-owned
directories. Runtime-specific lowercase names required by Podman, Grafana, PostgreSQL, or metric
systems are allowed inside files when the platform requires them and must be documented near use.

## Complexity Tracking

No constitution violations requiring justification.

## Phase 0: Research Summary

Research decisions are captured in [research.md](./research.md). All technical unknowns from the
plan are resolved without adding external application-code libraries.

## Phase 1: Design Summary

Data entities, validation rules, and relationships are captured in [data-model.md](./data-model.md).
Interface contracts are captured under [contracts/](./contracts/). End-to-end validation scenarios
are captured in [quickstart.md](./quickstart.md).

## Post-Design Constitution Check

- **TDD**: PASS. Contracts and quickstart identify testable scenarios for formulas, dashboard
  states, validation failures, protected access, and daily run behavior.
- **SOLID / Clean Architecture**: PASS. Data model and contracts preserve separation between
  domain calculations and external adapters.
- **DRY / YAGNI**: PASS. No speculative features beyond requested dashboards, catalog, KPIs,
  forecasts, risks, and top consumers are planned.
- **PascalCase**: PASS with documented platform exceptions.
- **No New External Libraries**: PASS. Contracts avoid application-code package requirements.
- **Validation and Auth**: PASS. Protected views and validation boundaries are explicitly defined.
