# Quickstart: Enterprise Governance Platform

## Prerequisites

- Podman available on the host.
- Repository cloned and on `main`.
- Stack images built.
- No new external Python packages installed.

## 1. Validate the Repository

```bash
Scripts/ValidateStack.sh
Scripts/RunTests.sh
```

Expected outcome:

```text
Validacion del stack completada correctamente
OK
```

## 2. Start the Stack

```bash
Scripts/BuildImages.sh
Scripts/StartStack.sh
Scripts/StackStatus.sh
```

Expected outcome:

- PostgreSQL is healthy.
- VictoriaMetrics is healthy.
- ZabbixServer is healthy.
- ZabbixWeb is healthy.
- Grafana is healthy.
- CapacityEngine is completed successfully or ready for batch execution.

## 3. Generate Enterprise Verification Evidence

Planned validation command:

```bash
Scripts/GenerateEnterpriseVerificationData.sh --profile mixed --domains all --services 5 --components 50 --days 90 --load-id EnterpriseDemo001
```

Expected outcome:

- Inventory records exist for multiple technology domains.
- Business services map to technology components.
- Evidence records include available, missing, unknown, incomplete, and unverified states.
- Score assessments exist on a 0-100 range.
- Risk registry entries identify affected technologies and services.
- Recommendations are tied to risks and evidence.

## 4. Run Enterprise Assessment

Planned validation command:

```bash
Scripts/RunEnterpriseAssessment.sh --scope enterprise --evidence-window-days 90 --run-id EnterpriseRun001
```

Expected outcome:

```text
INFO: evaluacion enterprise completada
  run: EnterpriseRun001
  scope: enterprise
  scores: <count>
  risks: <count>
  recomendaciones: <count>
```

## 5. Validate Governance Outputs

Planned validation command:

```bash
Scripts/ValidateEnterpriseGovernance.sh --run-id EnterpriseRun001
```

Expected outcome:

```text
INFO: validacion enterprise completada
  inventario: OK
  evidencia: OK
  scoring: OK
  riesgos: OK
  dashboards: OK
```

## 6. Review Dashboards

Open Grafana:

```text
http://localhost:3000
```

Expected dashboard behavior:

- Executive dashboard shows Technology Health Score and domain scores.
- Risk heat map shows risk by technology domain.
- Top risks include affected technologies, affected services, severity, impact, and recommended
  action.
- Missing or incomplete evidence is visible and not treated as healthy.
- Operational dashboards show trends, forecast horizons, top consumers, and evidence freshness.

## 7. Cleanup Verification Data

Planned validation command:

```bash
Scripts/GenerateEnterpriseVerificationData.sh delete --load-id EnterpriseDemo001
```

Expected outcome:

- Generated verification records are removed.
- Non-generated operational inventory and manually managed evidence remain intact.

## References

- [Data model](./data-model.md)
- [CLI contract](./contracts/cli-contract.md)
- [Dashboard contract](./contracts/dashboard-contract.md)
- [Dataset contract](./contracts/dataset-contract.md)
