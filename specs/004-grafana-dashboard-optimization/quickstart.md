# Quickstart: Grafana Dashboard Optimization

## Prerequisites

- Current branch: `004-grafana-dashboard-optimization`
- Local images already built or available.
- Podman available for runtime validation.
- Existing stack ports available: Grafana `3000`, Zabbix Web `8080`, VictoriaMetrics `8428`, PostgreSQL `5432`, Zabbix Server `10051`.

## Validate Planning Artifacts

```bash
Scripts/RunTests.sh
Scripts/ValidateStack.sh
```

Expected outcome:

- All tests pass.
- Stack validation completes successfully.

## Start the Stack

```bash
Scripts/StopStack.sh
Scripts/StartStack.sh
Scripts/StackStatus.sh
```

Expected outcome:

- PostgreSQL, VictoriaMetrics, ZabbixServer, ZabbixWeb, and Grafana are healthy.
- CapacityEngine may show completed successfully because it is a batch task.

## Generate Dashboard Verification Data

```bash
Scripts/GenerateVerificationBatches.sh DashboardOpt001
Scripts/ManageTestData.sh validate --load-id DashboardOpt001-critical
```

Expected outcome:

- PostgreSQL synthetic data validates as OK.
- VictoriaMetrics synthetic samples validate as OK.
- Zabbix hosts/items validate as OK when Zabbix is available.

## Validate Executive Dashboard Behavior

1. Open `http://localhost:3000`.
2. Authenticate with the configured Grafana credentials.
3. Open the `Capacity` folder.
4. Review the executive capacity dashboard.

Expected outcome:

- Overall capacity state is visible.
- Top risks are visible.
- Forecast for 30, 60, and 90 days is visible.
- Headroom and recommendations are visible.
- The `DashboardOpt001-critical` scenario is sufficient to show a critical decision state.

## Validate Technical Dashboard Behavior

1. Open the technical performance dashboard in the `Capacity` folder.
2. Review metric panels and KPI tables.

Expected outcome:

- CPU, memory, storage, IOPS, network, latency, throughput, errors, and saturation are represented.
- Affected resource and metric context is visible.
- Warning or critical states can be traced to service or resource context.

## Validate Planning and Service Context

1. Open the capacity planning dashboard.
2. Open the application or service dashboard.

Expected outcome:

- Monthly growth, headroom, baseline comparison, and days to saturation are visible.
- Service, application, infrastructure, and dependency context are visible.
- Overprovisioned and underprovisioned categories can be identified when represented by the scenario data.

## Empty-State Validation

```bash
Scripts/ManageTestData.sh delete --load-id DashboardOpt001-critical
Scripts/ManageTestData.sh validate --load-id DashboardOpt001-critical
```

Expected outcome:

- Validation reports no data for the deleted load.
- Dashboards do not imply that missing data means an OK condition.

## Troubleshooting

Check Grafana status and logs:

```bash
Scripts/StackStatus.sh Grafana
Scripts/StackLogs.sh Grafana 100
```

Check VictoriaMetrics sample visibility:

```bash
curl "http://localhost:8428/api/v1/query?query=count_over_time%28synthetic_cpu%7Bload_id%3D%22DashboardOpt001-critical%22%7D%5B400d%5D%29"
```
