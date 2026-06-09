# Capacity and Performance

Stack self-hosted para monitoreo tecnico, observabilidad de capacidad y administracion operativa de
imagenes con Podman, Zabbix, VictoriaMetrics, Grafana, PostgreSQL y un motor de capacidad en Python.

El objetivo es ofrecer una arquitectura moderna, escalable y sin costos de licencias para visualizar
estado operativo, capacidad usada, riesgo de saturacion, forecast, top consumidores y relacion entre
servicios, aplicaciones e infraestructura.

## Administracion de Imagenes y Stack

Validar archivos requeridos:

```bash
Scripts/ValidateStack.sh
```

Ejecutar tests:

```bash
Scripts/RunTests.sh
```

Construir todas las imagenes:

```bash
Scripts/BuildImages.sh
```

Construir una imagen individual:

```bash
Scripts/BuildImages.sh Grafana v1.0.0
```

Iniciar el stack:

```bash
Scripts/StartStack.sh
```

`StartStack.sh` valida primero que existan todas las imagenes locales. Si falta alguna, ejecutar
`Scripts/BuildImages.sh` antes de iniciar.

Grafana monta `Config/Grafana/Datasources`, `Config/Grafana/DashboardProviders` y
`Config/Grafana/Dashboards` desde el repositorio. Despues de un `git pull`, reiniciar el stack
alcanza para reprovisionar dashboards y datasources sin reconstruir la imagen:

```bash
Scripts/StopStack.sh
Scripts/StartStack.sh
```

Consultar estado:

```bash
Scripts/StackStatus.sh
Scripts/StackStatus.sh Grafana
```

Consultar logs:

```bash
Scripts/StackLogs.sh Grafana 100
```

Detener el stack:

```bash
Scripts/StopStack.sh
```

Limpieza explicita de recursos temporales:

```bash
Scripts/CleanupStack.sh --confirmar
```

Modo simulacion sin ejecutar Podman:

```bash
STACK_DRY_RUN=1 Scripts/BuildImages.sh Grafana v1.0.0
STACK_DRY_RUN=1 Scripts/StartStack.sh
STACK_DRY_RUN=1 Scripts/StackStatus.sh
STACK_DRY_RUN=1 Scripts/StackLogs.sh Grafana 50
STACK_DRY_RUN=1 Scripts/ValidateLocalAccess.sh
STACK_DRY_RUN=1 Scripts/StopStack.sh
STACK_DRY_RUN=1 Scripts/CleanupStack.sh --confirmar
```

## Arquitectura Base de Observabilidad

Componentes:

- **ZabbixServer**: monitoreo de sistemas y subsistemas.
- **ZabbixWeb**: interfaz web de Zabbix.
- **ZabbixAgent**: agente con checks custom para levantar licencias, compliance, backlevel,
  lifecycle y fecha de fin de soporte por host.
- **VictoriaMetrics**: almacenamiento de metricas de series temporales.
- **Grafana**: capa principal de dashboards con metadata persistida en PostgreSQL.
- **PostgreSQL**: motor de base de datos comun para Zabbix, Grafana, catalogo, KPIs, forecasts,
  riesgos, recomendaciones y consistencia de datos.
- **CapacityEngine**: motor Python diario para calculo de capacidad.
- **Scripts**: administracion de build, start, stop, logs, status, cleanup y validacion.

Accesos locales:

```text
Grafana:          http://localhost:3000
Zabbix Web:       http://localhost:8080
VictoriaMetrics:  http://localhost:8428
PostgreSQL:       localhost:5432
Zabbix Server:    localhost:10051
```

Credenciales por defecto para Grafana:

```text
Usuario: admin
Password: admin
```

Credenciales por defecto para Zabbix Web:

```text
Usuario: Admin
Password: zabbix
```

Para una instancia remota de Ubuntu, reemplazar `localhost` por la IP publica o nombre DNS del
servidor, por ejemplo `http://IP_DEL_SERVIDOR:3000`. Abrir los puertos requeridos en el firewall del
sistema operativo y en las reglas de red del proveedor.

PostgreSQL y Zabbix Server no son endpoints HTTP. No se validan con `curl`; se acceden con clientes
especificos o desde otros contenedores del stack.

Validar acceso local con los protocolos correctos:

```bash
Scripts/ValidateLocalAccess.sh
Scripts/ValidateLocalAccess.sh IP_DEL_SERVIDOR
```

Validar consistencia del motor PostgreSQL:

```bash
Scripts/ValidateDatabaseConsistency.sh
```

La validacion confirma que Grafana usa PostgreSQL como base operacional (`grafana`) y que Zabbix,
catalogo, datos sinteticos y CapacityEngine usan el mismo motor PostgreSQL (`capacity`).

Interconexion interna del stack:

```text
Grafana -> capacity-performance-victoriametrics:8428
Grafana -> capacity-performance-postgresql:5432
Grafana metadata -> capacity-performance-postgresql:5432/grafana
ZabbixWeb -> capacity-performance-zabbix-server:10051
ZabbixWeb -> capacity-performance-postgresql:5432
ZabbixServer -> capacity-performance-postgresql:5432
ZabbixServer -> capacity-performance-zabbix-agent:10050
ManageTestData -> PostgreSQL, VictoriaMetrics y Zabbix
CapacityEngine -> PostgreSQL y VictoriaMetrics
```

Zabbix es la fuente del inventario de hosts. Cuando se da de alta, baja o modifica un equipo en
Zabbix, sincronizar el catalogo PostgreSQL para que Grafana y las consultas SQL reflejen el mismo
estado:

```bash
Scripts/SyncZabbixInventory.sh
```

La sincronizacion toma hosts `SRV-#####` desde Zabbix, actualiza `MonitoredResource` con
`Platform = ZabbixInventory` y elimina del catalogo los hosts de inventario que ya no existan en
Zabbix.

Ejecutar el motor diario de capacidad:

```bash
Scripts/RunCapacityDaily.sh
```

Salida esperada:

```text
Run-YYYYMMDDHHMMSS Succeeded resources=1
```

`CapacityEngine` es una tarea batch: si termino con exit code `0`, el estado esperado es
`salud: completado correctamente`. No queda escuchando un puerto ni ejecutandose permanentemente.

## Dashboards de Grafana

La provision de Grafana incluye vistas en la carpeta `Capacity`:

- Executive Capacity Dashboard
- Technical Performance Dashboard
- Capacity Planning Dashboard
- Application Dashboard
- Enterprise Executive Dashboard
- Enterprise Governance Dashboard
- Enterprise Operational Dashboard
- Enterprise License Compliance Dashboard
- Enterprise Software Backlevel Dashboard

Los dashboards cubren estado OK/Warning/Critical, forecast 30/60/90 dias, utilizacion promedio,
pico, percentil 95, headroom, dias a saturacion, baseline, SLA/SLO, dependencias y recomendaciones.

Uso recomendado:

- Cada dashboard incluye un cuadro visible `Como leer este dashboard` con `Que muestra`,
  `Como interpretarlo` y `Accion sugerida`.
- Cada dashboard incluye filtro `Lote`; `All` muestra todos los lotes cargados.
- Cada panel no textual incluye enlaces de drill-down. Al hacer click sobre un host, servicio o
  serie, usar `Ver graficos del equipo` para abrir `Technical Performance Dashboard` filtrado por
  `LoadId`, `HostName` y `ServiceId`.
- Cuando se filtra por equipo o subsistema, las series tecnicas muestran tres lineas: valor actual,
  average del rango seleccionado y tendencia lineal calculada sobre el mismo rango.
- **Executive Capacity Dashboard**: decision ejecutiva con estado general, top 5 riesgos,
  forecast 30/60/90, headroom y recomendaciones priorizadas.
- **Technical Performance Dashboard**: mejora operativa con CPU, RAM, storage, IOPS, red,
  latencia, throughput, errores, saturacion, percentil 95, top consumidores y outliers.
- **Capacity Planning Dashboard**: planificacion con crecimiento mensual, headroom, baseline,
  dias a saturacion, recursos sobredimensionados y subdimensionados.
- **Application Dashboard**: contexto de aplicacion con salud, infraestructura asociada,
  dependencias criticas y performance end-to-end.
- **Enterprise Executive Dashboard**: salud tecnologica consolidada, scores 0-100, top riesgos,
  evidencia faltante y prioridades ejecutivas.
- **Enterprise Governance Dashboard**: inventario, ciclo de vida, cumplimiento, confianza de
  monitoreo y registro de riesgos.
- **Enterprise Operational Dashboard**: tendencias, forecast 30/90/180/365, top consumidores y
  frescura de evidencia.
- **Enterprise License Compliance Dashboard**: licencias por host/servicio, estado compliant,
  non-compliant, unknown y acciones para auditoria.
- **Enterprise Software Backlevel Dashboard**: software backlevel, end-of-support, end-of-life,
  fecha de soporte y acciones de upgrade.

## Gobierno Enterprise

El feature enterprise agrega evaluaciones de salud tecnologica, riesgo, scoring, inventario,
ciclo de vida, cumplimiento y confianza de monitoreo. La evidencia faltante se muestra como tal y
nunca se interpreta como estado saludable.

Comandos previstos:

```bash
Scripts/RunEnterpriseAssessment.sh --scope enterprise
Scripts/ValidateEnterpriseGovernance.sh
Scripts/GenerateEnterpriseVerificationData.sh --profile mixed --volume small --days 90 --load-id EnterpriseDemo001
Scripts/ValidateEnterpriseGovernance.sh --load-id EnterpriseDemo001
```

La carga enterprise reutiliza el generador sintetico existente y agrega tablas enterprise en
PostgreSQL, datos de testing de licencias/backlevel/compliance/lifecycle, labels
`technology_domain`, `business_service` y `business_service_id` en VictoriaMetrics, y hosts
`SRV-#####` congruentes con el inventario de Zabbix.

En Zabbix, esos datos se ven por host en `Monitoring > Latest data` como items de agente:

```text
Enterprise Licencia - Estado
Enterprise Compliance - Estado
Enterprise Software Backlevel - Estado
Enterprise Lifecycle - Estado
Enterprise Software - Fecha fin de soporte
```

La fuente es `ZabbixAgent`, usando el UserParameter `capacity.enterprise.fact[HostName,FactName]`.
Despues de cargar datos, esperar el intervalo de polling del agente o ejecutar manualmente
`Check now` sobre los items si la UI lo permite.

Si Grafana muestra que PostgreSQL no tiene base por defecto configurada, actualizar y reiniciar:

```bash
git pull
Scripts/StopStack.sh
Scripts/StartStack.sh
```

## Datos Sinteticos e Historicos

Gestionar datos sinteticos de prueba:

```bash
Scripts/ManageTestData.sh load --profile mixed --volume small
Scripts/ManageTestData.sh load --profile critical --volume small --load-id DemoCritical001
Scripts/ManageTestData.sh list
Scripts/ManageTestData.sh validate
Scripts/ManageTestData.sh delete --load-id DemoCritical001
Scripts/ManageTestData.sh delete --all --confirmar
```

Generar lotes de verificacion para todas las herramientas:

```bash
Scripts/GenerateVerificationBatches.sh
Scripts/GenerateVerificationBatches.sh DemoFull001
```

Generar historia diaria aleatoria de 30, 60 y 90 dias para validar tendencias y forecast:

```bash
Scripts/GenerateHistoricalVerificationBatches.sh
Scripts/GenerateHistoricalVerificationBatches.sh HistoryFull001
```

Este script crea lotes como `HistoryFull001-30d-critical`, `HistoryFull001-60d-warning` y
`HistoryFull001-90d-mixed`. Cada lote contiene muestras diarias por recurso y metrica para que
Grafana y VictoriaMetrics tengan datos historicos suficientes en paneles de tendencia, percentil 95,
forecast 30/60/90, saturacion y capacity planning.

Los recursos sinteticos usan nombres de host con nomenclatura `SRV-#####`, por ejemplo `SRV-48291`.
Ese valor se usa como nombre visible y como host name tecnico en Zabbix, y tambien se guarda en el
catalogo PostgreSQL e inventario junto con asset tag, tipo, sistema operativo, ubicacion y notas del
lote.

La misma identidad de host queda disponible en todas las herramientas:

- Zabbix: `host` y nombre visible `SRV-#####`.
- PostgreSQL: `MonitoredResource.Name` como `SRV-#####`.
- VictoriaMetrics: etiqueta `host_name="SRV-#####"`.
- Grafana: columnas `HostName` y leyendas basadas en `{{host_name}}`.

`ResourceId` queda reservado como clave tecnica estable para relaciones, borrado y correlacion
historica. Las vistas ejecutivas muestran `HostName` para que recomendaciones y riesgos sean
accionables por equipo.

Para inventario operativo, Zabbix gobierna altas, bajas y modificaciones. Ejecutar
`Scripts/SyncZabbixInventory.sh` despues de cambiar hosts en Zabbix para reflejar el cambio en
PostgreSQL y Grafana.

En Zabbix se crean hosts sinteticos con items, inventario, graficos por host y triggers
Warning/Critical para validar alertamientos. Revisar:

```text
Grupo: Capacity Synthetic
Hosts: SRV-#####
Graficos: Capacity Synthetic - SRV-#####
Triggers: Capacity Synthetic Warning/Critical ...
```

Validar una carga:

```bash
Scripts/ManageTestData.sh validate --load-id HistoryFull001-90d-critical
```

Validar una serie sintetica en VictoriaMetrics:

```bash
curl "http://localhost:8428/api/v1/query?query=count_over_time%28synthetic_cpu%7Bload_id%3D%22HistoryFull001-90d-critical%22%7D%5B400d%5D%29"
```

## Estructura

```text
CapacityEngine/       Motor de capacidad en Python
Config/               Configuracion del stack y provision de Grafana
ContainerImages/      Containerfiles por componente
Scripts/              Comandos operativos
Sql/                  Esquemas, seed y validaciones SQL
Tests/                Pruebas unitarias, contract e integracion
docs/                 Documentacion operativa
specs/                Especificaciones Spec Kit
```

## Validacion Actual

La implementacion fue validada con:

```text
Scripts/RunTests.sh        -> suite OK
Scripts/ValidateStack.sh   -> OK
STACK_DRY_RUN=1 scripts operativos -> OK
```
