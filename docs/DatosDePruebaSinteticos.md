# Datos de Prueba Sinteticos

El stack incluye un comando operativo para generar, listar, validar y borrar datos sinteticos de
monitoreo, performance y capacity. El objetivo es validar dashboards y herramientas instaladas sin
usar mediciones reales.

Cuando el stack esta iniciado, la carga escribe datos en PostgreSQL para los paneles SQL de Grafana,
publica series en VictoriaMetrics para los paneles tecnicos y crea hosts/items sinteticos en Zabbix.
En `STACK_DRY_RUN=1`, la carga queda limitada al almacenamiento local de prueba.

## Cargar Datos

```bash
Scripts/ManageTestData.sh load --profile mixed --volume small
Scripts/ManageTestData.sh load --profile critical --volume small --load-id DemoCritical001
```

Generar una bateria de lotes para verificar todas las vistas:

```bash
Scripts/GenerateVerificationBatches.sh
Scripts/GenerateVerificationBatches.sh DemoFull001
```

El script genera lotes `normal`, `warning`, `critical` y `mixed`. Para Zabbix usa la API web
en `http://localhost:8080/api_jsonrpc.php` con `ZABBIX_USER=Admin` y `ZABBIX_PASSWORD=zabbix`
por defecto.

Los dashboards optimizados se validan con esos cuatro perfiles:

- `normal`: confirma estado OK y headroom disponible.
- `warning`: confirma alertas preventivas y recursos con crecimiento.
- `critical`: confirma top 5 de riesgos, forecast 30/60/90 y recomendaciones ejecutivas.
- `mixed`: confirma comparacion tecnica, outliers, sobredimensionamiento y subdimensionamiento.

En Grafana, cada dashboard incluye un cuadro informativo inicial `Como leer este dashboard`. Ese
cuadro explica que muestra la vista, como interpretar los resultados y que accion sugerida tomar.

Antes de recrear cada lote, el script intenta borrar el lote con el mismo identificador para que la
ejecucion sea repetible. Si Zabbix rechaza muestras historicas por permisos o cache de configuracion,
la carga continua con hosts/items sinteticos creados para validar `Monitoring > Latest data`.

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
ademas de presencia de datos sinteticos en PostgreSQL, VictoriaMetrics y Zabbix.

Validar una serie publicada en VictoriaMetrics:

```bash
curl "http://localhost:8428/api/v1/query?query=count_over_time%28synthetic_cpu%7Bload_id%3D%22DemoCritical001%22%7D%5B400d%5D%29"
```

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
