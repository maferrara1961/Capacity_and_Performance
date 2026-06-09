# Quickstart: Datos de Prueba para Monitoreo, Performance y Capacity

## Prerequisites

```bash
Scripts/BuildImages.sh
Scripts/StartStack.sh
Scripts/ValidateLocalAccess.sh
```

Expected result: Grafana, Zabbix Web and VictoriaMetrics respond through HTTP; PostgreSQL and Zabbix Server accept TCP connections.

## Run Tests First

```bash
Scripts/RunTests.sh
Scripts/ValidateStack.sh
```

Expected result: all tests pass and stack validation reports OK.

## Standard Load

```bash
Scripts/ManageTestData.sh load --profile mixed --volume small
```

Expected result:
- A new load id is reported.
- The summary includes services, resources, metric samples, KPIs, forecasts, risks and recommendations.
- Dashboards have backing data for executive, technical, capacity planning and application views.

## Multiple Loads

```bash
Scripts/ManageTestData.sh load --profile normal --volume small --load-id DemoNormal001
Scripts/ManageTestData.sh load --profile critical --volume small --load-id DemoCritical001
Scripts/ManageTestData.sh list
```

Expected result: both load ids are visible and independently traceable.

## Validate Tools and Data

```bash
Scripts/ManageTestData.sh validate
Scripts/ManageTestData.sh validate --load-id DemoCritical001
```

Expected result: the command reports availability and data checks for installed tools and the selected load.

## Delete One Load

```bash
Scripts/ManageTestData.sh delete --load-id DemoNormal001
Scripts/ManageTestData.sh list
```

Expected result: `DemoNormal001` is removed or marked deleted while `DemoCritical001` remains available.

## Delete All Test Loads

```bash
Scripts/ManageTestData.sh delete --all --confirmar
Scripts/ManageTestData.sh list
```

Expected result: all synthetic test loads are removed, stack configuration and non-test data are preserved.

## Invalid Input Checks

```bash
Scripts/ManageTestData.sh load --profile invalido
Scripts/ManageTestData.sh delete --all
Scripts/ManageTestData.sh delete --load-id "../unsafe"
```

Expected result: each command fails before modifying data and prints a deterministic Spanish error.
