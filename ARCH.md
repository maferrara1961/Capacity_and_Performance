# Arquitectura de Capacity and Performance

Este documento describe las herramientas del stack, su comunicacion interna, los subsistemas
principales y las bases de datos asociadas.

## Vista General

```text
Usuario / Operador
  |
  | HTTP 3000
  v
Grafana
  |-- HTTP 8428 ------------------> VictoriaMetrics
  |-- TCP 5432 -------------------> PostgreSQL
  |
  v
Dashboards Capacity

Usuario / Operador
  |
  | HTTP 8080
  v
ZabbixWeb
  |-- TCP 10051 ------------------> ZabbixServer
  |-- TCP 5432 -------------------> PostgreSQL

CapacityEngine / ManageTestData
  |-- TCP 5432 -------------------> PostgreSQL
  |-- HTTP 8428 ------------------> VictoriaMetrics
  |-- HTTP 8080 API JSON-RPC -----> ZabbixWeb
```

Todos los contenedores se conectan a la red interna:

```text
capacity-performance-net
```

## Herramientas

| Herramienta | Contenedor | Puerto | Funcion |
|---|---:|---:|---|
| PostgreSQL | `capacity-performance-postgresql` | `5432` | Persistencia relacional del catalogo, KPIs, forecasts, riesgos, recomendaciones y datos de prueba. |
| VictoriaMetrics | `capacity-performance-victoriametrics` | `8428` | Almacenamiento de series temporales sinteticas y metricas de performance. |
| ZabbixServer | `capacity-performance-zabbix-server` | `10051` | Motor de monitoreo Zabbix, items, triggers y procesamiento de datos. |
| ZabbixWeb | `capacity-performance-zabbix-web` | `8080` | Consola web/API JSON-RPC de Zabbix. |
| Grafana | `capacity-performance-grafana` | `3000` | Capa principal de dashboards ejecutivos, tecnicos, capacity planning y aplicacion. |
| CapacityEngine | `capacity-performance-capacity-engine` | sin puerto | Tarea batch Python para calculo de capacidad. |

## Comunicacion Interna

| Origen | Destino | Protocolo | Uso |
|---|---|---|---|
| Grafana | VictoriaMetrics | HTTP `8428` | Consultas PromQL sobre metricas sinteticas. |
| Grafana | PostgreSQL | TCP `5432` | Consultas SQL para KPIs, forecast, riesgos, recomendaciones y catalogo. |
| ZabbixWeb | ZabbixServer | TCP `10051` | Consola web conectada al motor Zabbix. |
| ZabbixWeb | PostgreSQL | TCP `5432` | Persistencia de configuracion y datos de Zabbix. |
| ZabbixServer | PostgreSQL | TCP `5432` | Persistencia operativa de Zabbix. |
| ManageTestData | PostgreSQL | `podman exec` + `psql` | Carga y borrado de catalogo, KPIs y forecasts sinteticos. |
| ManageTestData | VictoriaMetrics | HTTP API | Importacion y borrado de series temporales sinteticas. |
| ManageTestData | ZabbixWeb | HTTP JSON-RPC | Creacion de hosts, inventario, items, graficos y triggers sinteticos. |
| SyncZabbixInventory | ZabbixWeb | HTTP JSON-RPC | Lectura de inventario de hosts administrado por Zabbix. |
| SyncZabbixInventory | PostgreSQL | `podman exec` + `psql` | Alta, baja y modificacion de `MonitoredResource` segun inventario Zabbix. |
| CapacityEngine | PostgreSQL | TCP `5432` | Escritura/lectura prevista de resultados de capacidad. |
| CapacityEngine | VictoriaMetrics | HTTP `8428` | Lectura prevista de metricas de series temporales. |

## Subsistemas

### Administracion de Imagenes

Scripts principales:

- `Scripts/BuildImages.sh`
- `Scripts/StartStack.sh`
- `Scripts/StopStack.sh`
- `Scripts/StackStatus.sh`
- `Scripts/StackLogs.sh`
- `Scripts/CleanupStack.sh`
- `Scripts/ValidateStack.sh`
- `Scripts/ValidateLocalAccess.sh`

Responsabilidades:

- Construir imagenes locales Podman.
- Iniciar y detener contenedores en orden.
- Validar puertos, red, dependencias y archivos requeridos.
- Mantener volumenes persistentes salvo limpieza explicita.

### Observabilidad Tecnica

Herramientas:

- ZabbixServer
- ZabbixWeb
- VictoriaMetrics

Responsabilidades:

- Registrar hosts sinteticos `SRV-#####`.
- Mantener items, graficos y triggers Warning/Critical en Zabbix.
- Almacenar series temporales en VictoriaMetrics.
- Exponer metricas por `load_id`, `resource_id` y `host_name`.

### Catalogo y Capacidad

Herramienta principal:

- PostgreSQL

Tablas principales:

- `Service`
- `Application`
- `MonitoredResource`
- `ServiceResourceMap`
- `AlertThreshold`
- `Baseline`
- `CapacityRun`
- `CapacityKpi`
- `ForecastResult`
- `RiskAssessment`
- `Recommendation`
- `TestLoad`
- `TestDataRecordMap`

Responsabilidades:

- Mapear servicios, aplicaciones, recursos e infraestructura.
- Reflejar el inventario operativo gobernado por Zabbix.
- Guardar KPIs de capacidad.
- Guardar forecast 30/60/90 dias.
- Guardar riesgos y recomendaciones.
- Registrar lotes sinteticos de prueba.

Zabbix gobierna altas, bajas y modificaciones de hosts. PostgreSQL mantiene una copia sincronizada
en `MonitoredResource` para que Grafana pueda consultar el inventario junto con KPIs y forecasts.

### Dashboards

Herramienta principal:

- Grafana

Dashboards provisionados:

- `Executive Capacity Dashboard`
- `Technical Performance Dashboard`
- `Capacity Planning Dashboard`
- `Application Dashboard`

Datasources:

- `VictoriaMetrics`
- `CapacityPostgreSQL`

Identidad comun de hosts:

```text
Zabbix host/name           -> SRV-#####
PostgreSQL Resource.Name   -> SRV-#####
VictoriaMetrics host_name  -> SRV-#####
Grafana HostName           -> SRV-#####
```

### Datos Sinteticos

Scripts principales:

- `Scripts/ManageTestData.sh`
- `Scripts/GenerateVerificationBatches.sh`
- `Scripts/GenerateHistoricalVerificationBatches.sh`

Responsabilidades:

- Generar servicios, aplicaciones y recursos sinteticos.
- Generar hosts `SRV-#####` con inventario.
- Generar muestras diarias de 30, 60 y 90 dias.
- Cargar datos en PostgreSQL, VictoriaMetrics y Zabbix.
- Borrar datos sinteticos por lote o de forma total con confirmacion.

## Bases de Datos y Persistencia

| Componente | Persistencia | Volumen | Datos |
|---|---|---|---|
| PostgreSQL | Base `capacity` | `capacity-performance-postgresql-data` | Catalogo, KPIs, forecasts, riesgos, recomendaciones, lotes de prueba. |
| VictoriaMetrics | TSDB interna | `capacity-performance-victoriametrics-data` | Series temporales sinteticas por metrica, lote y host. |
| ZabbixServer/ZabbixWeb | PostgreSQL `capacity` | `capacity-performance-postgresql-data` y `capacity-performance-zabbix-server-data` | Configuracion Zabbix, hosts, items, triggers, graficos y datos operativos. |
| Grafana | SQLite interna | `capacity-performance-grafana-data` | Estado de Grafana; dashboards y datasources se reprovisionan desde `Config/Grafana`. |
| CapacityEngine | Sin persistencia propia | sin volumen dedicado | Tarea batch; resultados previstos en PostgreSQL. |

## Identificadores de Datos

| Campo | Herramienta | Proposito |
|---|---|---|
| `LoadId` / `load_id` | PostgreSQL, VictoriaMetrics, Grafana | Identificar lote sintetico y filtrar dashboards. |
| `ResourceId` / `resource_id` | PostgreSQL, VictoriaMetrics | Identificador tecnico estable para relaciones y borrado. |
| `HostName` / `host_name` | PostgreSQL, VictoriaMetrics, Grafana | Nombre operativo comun `SRV-#####`. |
| `host` | Zabbix | Host tecnico y visible `SRV-#####`. |
| `asset_tag` | Zabbix inventory | Relacionar host con lote y permitir limpieza por `LoadId`. |

## Flujo de Sincronizacion de Inventario

```text
Alta / baja / modificacion de host en Zabbix
  -> Scripts/SyncZabbixInventory.sh
      -> Zabbix API host.get + inventory
      -> PostgreSQL MonitoredResource
          -> upsert de hosts existentes
          -> delete de hosts Platform=ZabbixInventory que ya no existen en Zabbix
      -> Grafana
          -> dashboards SQL consultan inventario sincronizado
```

Regla de consistencia:

```text
Zabbix host SRV-##### == PostgreSQL MonitoredResource.Name == Grafana HostName
```

## Flujo de Carga Sintetica

```text
GenerateHistoricalVerificationBatches.sh
  -> ManageTestData.sh load
      -> SyntheticDataService
          -> genera servicios, aplicaciones, recursos SRV-#####, muestras, KPIs y forecast
      -> SyntheticPostgreSqlAdapter
          -> inserta catalogo, KPIs, forecast, riesgos, recomendaciones y TestLoad
      -> SyntheticVictoriaMetricsAdapter
          -> publica series con load_id, resource_id y host_name
      -> SyntheticZabbixAdapter
          -> crea hosts SRV-#####, inventario, items, graficos, triggers e historia
```

## Puertos Publicados

| Servicio | Puerto local | Uso |
|---|---:|---|
| Grafana | `3000` | Dashboards web. |
| ZabbixWeb | `8080` | Consola/API Zabbix. |
| VictoriaMetrics | `8428` | UI/API VictoriaMetrics. |
| PostgreSQL | `5432` | Cliente SQL y conexiones internas. |
| ZabbixServer | `10051` | Protocolo Zabbix server. |

PostgreSQL y ZabbixServer no son endpoints HTTP.

## Seguridad Operativa

- Dashboards protegidos por autenticacion Grafana.
- Zabbix Web protegido por autenticacion Zabbix.
- Entradas de scripts validadas por listas de servicios permitidos y confirmacion en operaciones destructivas.
- No se agregan librerias externas al codigo Python de aplicacion.
- Los datos de prueba se marcan y limpian por lote para evitar borrar datos no sinteticos.
