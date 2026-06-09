# Datos de Prueba Sinteticos

El stack incluye un comando operativo para generar, listar, validar y borrar datos sinteticos de
monitoreo, performance y capacity. El objetivo es validar dashboards y herramientas instaladas sin
usar mediciones reales.

Cuando el stack esta iniciado, la carga escribe datos en PostgreSQL para los paneles SQL de Grafana
y publica series en VictoriaMetrics para los paneles tecnicos. En `STACK_DRY_RUN=1`, la carga queda
limitada al almacenamiento local de prueba.

## Cargar Datos

```bash
Scripts/ManageTestData.sh load --profile mixed --volume small
Scripts/ManageTestData.sh load --profile critical --volume small --load-id DemoCritical001
```

Perfiles permitidos:

```text
normal
warning
critical
overprovisioned
underprovisioned
mixed
```

Volumenes permitidos:

```text
small
medium
large
```

## Listar Cargas

```bash
Scripts/ManageTestData.sh list
Scripts/ManageTestData.sh list --status Succeeded
```

## Validar Datos y Herramientas

```bash
Scripts/ManageTestData.sh validate
Scripts/ManageTestData.sh validate --load-id DemoCritical001
```

La validacion informa estado de Grafana, Zabbix Web, VictoriaMetrics, PostgreSQL y Zabbix Server,
ademas de presencia de datos sinteticos.

## Borrar Datos

Borrar un lote:

```bash
Scripts/ManageTestData.sh delete --load-id DemoCritical001
```

Borrar todos los lotes sinteticos:

```bash
Scripts/ManageTestData.sh delete --all --confirmar
```

El borrado total exige `--confirmar`. Las operaciones de limpieza estan limitadas a datos marcados
como sinteticos.

## Modo de Prueba

Para validar comandos sin depender del stack real:

```bash
STACK_DRY_RUN=1 Scripts/ManageTestData.sh load --profile mixed --volume small
STACK_DRY_RUN=1 Scripts/ManageTestData.sh delete --all --confirmar
```
