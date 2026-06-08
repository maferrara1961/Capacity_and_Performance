# Quickstart: Capacity Observability Stack

## Purpose

Use this guide to validate the feature end-to-end after implementation tasks are generated and
completed. The guide focuses on observable outcomes, not implementation internals.

## Prerequisites

- Linux host with Podman available.
- Access to the project repository.
- Test credentials for an authenticated operator.
- Sample services, resources, thresholds, baselines, and metric data.

## 1. Validate Stack Definition

Run the stack validation command.

```bash
Scripts/ValidateStack.sh
```

Expected outcome:
- Required Podman image definitions are present for Zabbix, VictoriaMetrics, Grafana, PostgreSQL,
  and CapacityEngine.
- No unapproved application-code dependencies are reported.
- Grafana datasource and dashboard provisioning files are present.

## 2. Start the Stack

```bash
Scripts/StartStack.sh
```

Expected outcome:
- Monitoring, metrics, dashboard, persistence, and capacity engine services start successfully.
- Protected dashboard access requires authentication.
- Unauthenticated access to dashboards and catalog views is rejected.

## 3. Load Sample Catalog and Metrics

Load sample validation data using the implemented seed or validation scripts.

```bash
Scripts/ValidateStack.sh --load-sample-data
```

Expected outcome:
- Services, applications, resources, thresholds, and baselines are available.
- At least one service is healthy.
- At least one service is at Warning or Critical capacity risk.
- At least one service has incomplete catalog mapping for edge-case validation.

## 4. Run Daily Capacity Calculation

```bash
Scripts/RunCapacityDaily.sh
```

Expected outcome:
- A successful capacity run is recorded.
- KPI results include average, peak, p95, monthly growth, headroom, and baseline comparison.
- Forecast results include 30, 60, and 90 day projections.
- Risks are classified for CPU, RAM, storage, IOPS, and network.
- Top consumers are calculated.

## 5. Validate Executive Dashboard

Open the Executive Capacity Dashboard as an authenticated user.

Expected outcome:
- Overall state is OK, Warning, or Critical.
- Top 10 saturation risks are visible.
- Forecasts for 30, 60, and 90 days are visible where enough history exists.
- Recommendations are visible for Warning and Critical risks.

## 6. Validate Technical Dashboard

Open the Technical Performance Dashboard.

Expected outcome:
- CPU, memory, disk, network, IOPS, latency, throughput, errors, and saturation are visible.
- Average, peak, and p95 values are visible.
- Threshold breaches are visually indicated.
- Users can drill from risky service to affected resource.

## 7. Validate Capacity Planning Dashboard

Open the Capacity Planning Dashboard.

Expected outcome:
- Historical trends and monthly growth are visible.
- Estimated exhaustion dates are visible for growing resources.
- Oversized and undersized resources are listed.
- Headroom and baseline comparison are visible.

## 8. Validate Application Dashboard

Open the Application Dashboard.

Expected outcome:
- Application health, associated infrastructure, SLA/SLO status, end-to-end performance, and
  critical dependencies are visible.
- A degraded critical dependency affects application risk state.

## 9. Validate Failure and Edge Cases

Run validation scenarios for:
- Insufficient historical data.
- Missing catalog mapping.
- Duplicate metric samples.
- Malformed thresholds.
- Failed daily capacity run.
- Unauthenticated dashboard access.

Expected outcome:
- Invalid inputs are rejected deterministically.
- Insufficient data produces Unknown or Low confidence instead of false precision.
- Previous successful capacity results remain visible after a failed run with stale-state warning.
