# Research: Capacity Observability Stack

## Decision: Self-hosted platform components are accepted as requested runtime components

**Rationale**: The feature explicitly requires Podman images for Zabbix, VictoriaMetrics, Grafana,
PostgreSQL, and a Python capacity engine. Treating these as requested platform components satisfies
the user goal while preserving the constitution restriction against additional libraries, SDKs,
hosted services, or license-cost services.

**Alternatives considered**:
- Add hosted monitoring services: rejected because the user requested no license-cost architecture.
- Add application-code packages for convenience: rejected by constitution.
- Build every capability from scratch: rejected because requested platform components already
  provide monitoring, metrics storage, dashboarding, and persistence roles.

## Decision: Python capacity engine uses standard library only

**Rationale**: The constitution prohibits new external application-code libraries. The engine can
keep calculation logic in pure Python and interact with persistence through generated SQL files,
validated inputs, and platform command adapters rather than client packages.

**Alternatives considered**:
- Use a PostgreSQL client package: rejected as an external application-code dependency.
- Put all calculations directly in SQL: rejected because the user requested a Python capacity
  engine and because domain formulas need focused unit tests.
- Use advanced forecasting libraries: rejected for initial scope and dependency discipline.

## Decision: Clean Architecture boundary around capacity domain

**Rationale**: Capacity KPIs, growth, forecast, risk scoring, top consumers, service mapping, and
recommendations are domain/application behavior. Podman, Grafana, Zabbix, VictoriaMetrics,
PostgreSQL, and scheduler execution are adapters. This preserves testability and prevents platform
details from leaking into formulas.

**Alternatives considered**:
- Place formulas in dashboard queries only: rejected because it duplicates logic and makes tests
  brittle.
- Couple formulas to database schema directly: rejected because it weakens domain tests.
- Use a single orchestration script for everything: rejected because it violates separation of
  concerns for the requested feature size.

## Decision: Store catalog and calculated capacity outputs in PostgreSQL

**Rationale**: The service catalog, thresholds, baselines, forecasts, recommendations, and run
history are relational and need consistent validation and reporting. PostgreSQL is explicitly
requested and fits those durable records.

**Alternatives considered**:
- Store catalog in Grafana dashboard variables only: rejected because catalog state must be durable
  and validateable.
- Store catalog in flat files only: rejected because relationships and history are first-class.
- Store all derived results only in time-series storage: rejected because recommendations, owners,
  dependencies, and risk state are relational.

## Decision: Keep raw metrics and dashboard visualizations separate from derived KPIs

**Rationale**: The user explicitly asked not to show only raw metrics. Raw metrics remain useful for
technical troubleshooting, while calculated KPIs drive executive and planning views.

**Alternatives considered**:
- Raw-metric-only dashboards: rejected by the specification.
- Derived-KPI-only dashboards: rejected because technical users need CPU, memory, disk, network,
  latency, throughput, errors, and saturation.
- Duplicate KPI formulas per dashboard: rejected by DRY.

## Decision: Daily forecast windows are 30, 60, and 90 days

**Rationale**: The user explicitly requested those windows. Daily calculation is enough for the
initial planning workflow and reduces operational complexity.

**Alternatives considered**:
- Real-time forecasting: rejected as out of initial scope.
- Weekly-only calculation: rejected because the user requested daily calculation.
- Arbitrary custom windows in v1: rejected by YAGNI; configurable thresholds are enough for now.

## Decision: Dashboard families are contract-driven

**Rationale**: Executive, technical, capacity planning, and application dashboards need consistent
inputs, KPIs, filters, states, and protected access. Contracts make dashboards testable before
implementation.

**Alternatives considered**:
- Create ad hoc dashboards without contracts: rejected because tests and future tasks would be
  ambiguous.
- Collapse all views into one dashboard: rejected because executive and technical users have
  different workflows.

## Decision: Authentication protects all dashboard and catalog views

**Rationale**: The constitution requires protected routes to require authentication. The feature
contains capacity, service, dependency, and operational risk data, so all views and actions are
protected by default.

**Alternatives considered**:
- Public read-only executive dashboard: rejected because service risk data is operationally
  sensitive.
- Protect only catalog writes: rejected by constitution and feature assumptions.
