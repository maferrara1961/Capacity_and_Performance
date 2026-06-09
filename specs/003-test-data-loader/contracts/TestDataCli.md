# Contract: Test Data CLI

## Command

```bash
Scripts/ManageTestData.sh <action> [options]
```

The wrapper invokes the Python command and prints messages in Spanish.

## Actions

### load

Generates one synthetic test load.

```bash
Scripts/ManageTestData.sh load --profile mixed --volume small
Scripts/ManageTestData.sh load --profile critical --volume medium --load-id DemoCritical001
Scripts/ManageTestData.sh load --profile normal --days 90 --seed 12345
```

**Required behavior**:
- Validate stack/tool availability before writing.
- Reject invalid profile, volume, days, seed, or load id.
- Generate a unique load id when none is supplied.
- Print a Spanish summary with created counts.
- Exit `0` only when the load completed.

### list

Lists synthetic loads.

```bash
Scripts/ManageTestData.sh list
Scripts/ManageTestData.sh list --status Succeeded
```

**Required behavior**:
- Show load id, profile, status, created timestamp, generated counts, and cleanup status.
- Exit `0` when the listing succeeds, even if no loads exist.

### validate

Validates installed tools and synthetic data presence.

```bash
Scripts/ManageTestData.sh validate
Scripts/ManageTestData.sh validate --load-id DemoCritical001
```

**Required behavior**:
- Validate HTTP tools with HTTP checks.
- Validate non-HTTP tools with TCP or command-safe checks.
- Confirm dashboards have non-empty backing data after a load.
- Print clear Spanish results per tool/component.

### delete

Deletes synthetic data.

```bash
Scripts/ManageTestData.sh delete --load-id DemoCritical001
Scripts/ManageTestData.sh delete --all --confirmar
```

**Required behavior**:
- `--load-id` deletes only that load.
- `--all` requires `--confirmar`.
- Delete operations never remove unmarked operational data.
- Print deleted counts and affected load ids.

## Options

| Option | Applies To | Validation |
|--------|------------|------------|
| `--load-id <id>` | load, validate, delete | Required pattern: letters, numbers, dash, underscore; bounded length |
| `--profile <profile>` | load | `normal`, `warning`, `critical`, `overprovisioned`, `underprovisioned`, `mixed` |
| `--volume <volume>` | load | `small`, `medium`, `large` |
| `--days <number>` | load | Positive integer within bounded history window |
| `--seed <number>` | load | Positive integer for repeatable random generation |
| `--status <status>` | list | Known load status |
| `--all` | delete | Requires `--confirmar` |
| `--confirmar` | delete | Required for destructive all-load cleanup |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Operation completed successfully |
| `1` | Validation error or rejected input |
| `2` | Required tool unavailable |
| `3` | Load or delete partially completed and needs cleanup |

## Output Contract

Successful load includes:

```text
INFO: carga sintetica completada
  lote: <LoadId>
  perfil: <ScenarioProfile>
  servicios: <count>
  recursos: <count>
  muestras: <count>
  kpis: <count>
  forecasts: <count>
  riesgos: <count>
  recomendaciones: <count>
```

Successful delete includes:

```text
INFO: limpieza sintetica completada
  lotes eliminados: <count>
  registros eliminados: <count>
```

Errors must be deterministic and in Spanish.
