# Dashboard Contract: Enterprise Governance Platform

## Executive Dashboard

The executive dashboard must allow an executive user to understand enterprise technology health
within sixty seconds.

### Required Panels

- Technology Health Score.
- Capacity Score.
- Performance Score.
- Availability Score.
- Lifecycle Score.
- Compliance Score.
- Monitoring Confidence Score.
- Risk Heat Map by technology domain.
- Top 10 Risks with severity, impact, affected technologies, affected services, and action.
- Capacity Forecast for CPU, memory, and storage.
- Lifecycle Overview.
- Compliance Overview.
- Service Health Overview.
- Executive Decision Summary.

### Empty and Missing Evidence Behavior

- Missing evidence must display as missing, unknown, incomplete, or unverified.
- Missing evidence must not render as OK, Healthy, Compliant, or Supported.
- Dashboards must include enough context to distinguish "no risk" from "no evidence".

## Governance Dashboard

The governance dashboard supports service delivery managers, platform owners, and compliance users.

### Required Panels

- Technology inventory by domain.
- Service-to-component mapping.
- Lifecycle status by technology.
- Compliance status by technology.
- Monitoring coverage and freshness.
- Risk registry.
- Open recommendations by owner and severity.

## Operational Dashboard

The operational dashboard supports engineering and operations teams.

### Required Panels

- Capacity trends.
- Performance trends.
- Availability history.
- Top consumers.
- Saturation indicators.
- Forecast horizons for 30, 90, 180, and 365 days.
- Evidence freshness and collection failures.

## Filters

Dashboards must support, where data exists:

- Assessment run.
- Technology domain.
- Business service.
- Environment.
- Severity.
- Evidence state.

## Validation

Contract tests must inspect dashboard provisioning artifacts and confirm required titles, queries,
datasources, filters, and missing-evidence text are present.
