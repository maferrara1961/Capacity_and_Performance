# Contract: Verification Scenarios

## Purpose

Defines the expected behavior for repeatable dashboard verification scenarios.

## Scenario Profiles

### Normal

**Expected Result**:

- Executive dashboards show low or OK risk.
- Technical dashboards show stable performance signals.
- Planning dashboards show available headroom.

### Warning

**Expected Result**:

- Executive dashboards show at least one Warning condition.
- Technical dashboards show affected metrics and resources.
- Planning dashboards show reduced headroom or growth concern.

### Critical

**Expected Result**:

- Executive dashboards show at least one Critical condition.
- Forecast and days-to-saturation values are visible.
- Recommended action is visible.
- Technical dashboards show affected resource and metric context.

### Mixed

**Expected Result**:

- Dashboards show a combination of OK, Warning, and Critical states.
- Top consumers and outliers are identifiable.
- Service context remains visible across mixed states.

## Command Contract

The verification process must support:

- Loading a profile.
- Loading a named batch.
- Validating a named batch.
- Repeating a named verification batch without duplicate-identifier failure.
- Deleting verification data when requested.

## Validation Contract

For each named verification batch:

- PostgreSQL-backed capacity data must validate as present.
- VictoriaMetrics-backed performance samples must validate as present.
- Zabbix synthetic hosts/items should validate as present where Zabbix is available.
- Dashboard categories must have data coverage for executive and technical views.

## Input Validation Contract

- Load identifiers must reject unsafe, empty, malformed, or unsupported values.
- Profiles must be limited to approved scenario names.
- Volume choices must be limited to approved values.
