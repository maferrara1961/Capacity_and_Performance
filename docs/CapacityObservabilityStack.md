# Capacity Observability Stack

This stack provides self-hosted capacity observability with Podman, Zabbix, VictoriaMetrics,
Grafana, PostgreSQL, and a Python standard-library capacity engine.

## Validation

Run:

```bash
Scripts/RunTests.sh
Scripts/ValidateStack.sh
Scripts/RunCapacityDaily.sh
```

Expected result:

- Unit, contract, and integration tests pass.
- Stack definitions and dashboard provisioning files are present.
- Daily capacity calculation produces KPI, forecast, risk, and recommendation outputs.
