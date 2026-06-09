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

Generar datos historicos diarios para ventanas de 30, 60 y 90 dias:

```bash
Scripts/GenerateHistoricalVerificationBatches.sh
Scripts/GenerateHistoricalVerificationBatches.sh HistoryFull001
```

El script historico crea lotes por ventana y perfil, por ejemplo
`HistoryFull001-30d-normal`, `HistoryFull001-60d-warning` y `HistoryFull001-90d-critical`.
Cada lote incluye muestras diarias aleatorias por recurso y metrica para validar tendencias,
percentil 95, forecast 30/60/90, saturacion, capacity planning y paneles tecnicos en Grafana y
VictoriaMetrics.

Generar datos enterprise para validar los dashboards de salud tecnologica, gobierno y tendencias:

```bash
Scripts/GenerateEnterpriseVerificationData.sh --profile mixed --volume small --days 90 --load-id EnterpriseDemo001
Scripts/RunEnterpriseAssessment.sh --scope enterprise --load-id EnterpriseDemo001
Scripts/ValidateEnterpriseGovernance.sh --load-id EnterpriseDemo001
```

La carga enterprise agrega scores 0-100, riesgos, recomendaciones, evidencia, licencias,
compliance, software backlevel, lifecycle y labels `technology_domain`, `business_service` y
`business_service_id` en VictoriaMetrics. Tambien conserva la identidad `SRV-#####` en Zabbix,
PostgreSQL y Grafana.

En Zabbix, la informacion de licencias y software backlevel queda expuesta por el agente en
`Monitoring > Latest data` del host `SRV-#####`. Buscar estos items:

```text
Enterprise Licencia - Estado
Enterprise Compliance - Estado
Enterprise Software Backlevel - Estado
Enterprise Lifecycle - Estado
Enterprise Software - Fecha fin de soporte
```

El agente lee `.capacity-test-data/ZabbixAgent/EnterpriseFacts.tsv`, montado en el contenedor
`capacity-performance-zabbix-agent`, mediante `capacity.enterprise.fact[HostName,FactName]`.

Dashboards especificos para estos datos:

- `Enterprise License Compliance Dashboard`
- `Enterprise Software Backlevel Dashboard`

Para ver datos variados, usar `--volume medium` o `--volume large`; `small` crea pocos hosts y puede
mostrar menos combinaciones.

Los recursos se generan con host name `SRV-#####`, por ejemplo `SRV-48291`. Ese valor se usa como
nombre visible y como host tecnico en Zabbix, y queda registrado en PostgreSQL e inventario junto
con asset tag, tipo, sistema operativo, ubicacion y notas del lote.

La identidad del host es congruente entre herramientas: Zabbix usa `SRV-#####` como `host`,
PostgreSQL lo guarda en `MonitoredResource.Name`, VictoriaMetrics lo publica como etiqueta
`host_name` junto con `technology_domain` y `business_service`, y Grafana lo muestra como
`HostName` en tablas y leyendas.

Para inventario operativo, Zabbix es la fuente. Luego de alta, baja o modificacion manual de hosts
en Zabbix, ejecutar:

```bash
Scripts/SyncZabbixInventory.sh
```

Ese comando sincroniza `MonitoredResource` en PostgreSQL con el inventario actual de Zabbix.

Los dashboards de Grafana incluyen el filtro `Lote`. Seleccionar `All` muestra todos los lotes
cargados; seleccionar un lote como `HistoryFull001-90d-critical` filtra PostgreSQL y
VictoriaMetrics con el mismo identificador.

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
ejecucion sea repetible. En Zabbix se crean hosts, items, graficos por host y triggers
Warning/Critical para validar `Monitoring > Latest data`, `Monitoring > Hosts` y los alertamientos.
Las muestras historicas se publican por `itemid` para evitar rechazos por resolucion de host/key en
Zabbix.

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
