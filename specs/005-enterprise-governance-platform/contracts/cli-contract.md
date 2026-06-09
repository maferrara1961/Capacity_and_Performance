# CLI Contract: Enterprise Governance Platform

## Scope

This contract defines expected command behavior for enterprise assessment, validation, inventory
sync, and synthetic evidence generation. Command names may be implemented by extending existing
scripts or by adding new scripts, but behavior must remain testable from the shell.

## Common Rules

- Commands must validate all user-controlled arguments before execution.
- Commands must print Spanish operational messages consistent with existing scripts.
- Commands must return exit code `0` on success and non-zero on validation or execution failure.
- Destructive commands must require explicit confirmation.
- Commands must not require new external libraries.

## `Scripts/RunEnterpriseAssessment.sh`

Runs enterprise scoring and risk assessment for the selected scope.

### Required Arguments

- `--scope`: `enterprise`, `domain`, `service`, or `component`.

### Optional Arguments

- `--scope-id`: identifier required when scope is not `enterprise`.
- `--evidence-window-days`: positive integer; default `90`.
- `--run-id`: caller-supplied run id; generated if omitted.

### Success Output

```text
INFO: evaluacion enterprise completada
  run: <AssessmentRunId>
  scope: <scope>
  scores: <count>
  risks: <count>
  recomendaciones: <count>
```

### Validation Failures

- Unknown scope.
- Missing `--scope-id` for non-enterprise scope.
- Invalid evidence window.
- Missing required source containers or unavailable data source.

## `Scripts/ValidateEnterpriseGovernance.sh`

Validates that enterprise governance datasets and dashboards are usable.

### Optional Arguments

- `--run-id`: validate a specific assessment run.
- `--scope`: validate a specific scope.

### Success Output

```text
INFO: validacion enterprise completada
  inventario: OK
  evidencia: OK
  scoring: OK
  riesgos: OK
  dashboards: OK
```

## `Scripts/GenerateEnterpriseVerificationData.sh`

Generates representative enterprise evidence for inventory, telemetry, lifecycle, compliance,
monitoring confidence, risk, scoring, and dashboards.

### Optional Arguments

- `--profile`: `normal`, `warning`, `critical`, or `mixed`.
- `--domains`: comma-separated technology domains.
- `--services`: positive integer.
- `--components`: positive integer.
- `--days`: positive integer, default `90`.
- `--load-id`: caller-supplied dataset id.

### Delete Mode

```bash
Scripts/GenerateEnterpriseVerificationData.sh delete --load-id <LoadId>
Scripts/GenerateEnterpriseVerificationData.sh delete --all --confirmar
```

Delete mode must remove only generated enterprise verification data.
