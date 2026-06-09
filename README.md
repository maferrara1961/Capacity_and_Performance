# Capacity and Performance

Stack self-hosted para monitoreo tecnico, observabilidad de capacidad y administracion operativa de
imagenes con Podman, Zabbix, VictoriaMetrics, Grafana, PostgreSQL y un motor de capacidad en Python.

El objetivo es ofrecer una arquitectura moderna, escalable y sin costos de licencias para visualizar
estado operativo, capacidad usada, riesgo de saturacion, forecast, top consumidores y relacion entre
servicios, aplicaciones e infraestructura.

## Componentes

- **ZabbixServer**: monitoreo de sistemas y subsistemas.
- **ZabbixWeb**: interfaz web de Zabbix.
- **VictoriaMetrics**: almacenamiento de metricas de series temporales.
- **Grafana**: capa principal de dashboards.
- **PostgreSQL**: catalogo de servicios, umbrales, baselines, KPIs, forecasts y recomendaciones.
- **CapacityEngine**: motor Python diario para calculo de capacidad.
- **Scripts**: administracion de build, start, stop, logs, status, cleanup y validacion.

## Dashboards

La provision de Grafana incluye vistas para:

- Executive Capacity Dashboard
- Technical Performance Dashboard
- Capacity Planning Dashboard
- Application Dashboard

Los dashboards cubren estado OK/Warning/Critical, forecast 30/60/90 dias, utilizacion promedio,
pico, percentil 95, headroom, dias a saturacion, baseline, SLA/SLO, dependencias y recomendaciones.

Uso recomendado de dashboards:

- Cada dashboard incluye un cuadro visible `Como leer este dashboard` con tres partes:
  `Que muestra`, `Como interpretarlo` y `Accion sugerida`.
- **Executive Capacity Dashboard**: decision ejecutiva con estado general, top 5 riesgos,
  forecast 30/60/90, headroom y recomendaciones priorizadas.
- **Technical Performance Dashboard**: mejora operativa con CPU, RAM, storage, IOPS, red,
  latencia, throughput, errores, saturacion, percentil 95, top consumidores y outliers.
- **Capacity Planning Dashboard**: planificacion con crecimiento mensual, headroom, baseline,
  dias a saturacion, recursos sobredimensionados y subdimensionados.
- **Application Dashboard**: contexto de aplicacion con salud, infraestructura asociada,
  dependencias criticas y performance end-to-end.

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

## Uso rapido

Validar archivos requeridos:

```bash
Scripts/ValidateStack.sh
```

Ejecutar tests:

```bash
Scripts/RunTests.sh
```

Ejecutar el motor diario de capacidad:

```bash
Scripts/RunCapacityDaily.sh
```

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

El generador crea lotes `normal`, `warning`, `critical` y `mixed`. La carga escribe KPIs en
PostgreSQL para Grafana, series en VictoriaMetrics y hosts/items sinteticos en Zabbix.
El script borra primero cada lote con el mismo identificador para que pueda repetirse con el mismo
prefijo.

Generar historia diaria aleatoria de 30, 60 y 90 dias para validar tendencias y forecast:

```bash
Scripts/GenerateHistoricalVerificationBatches.sh
Scripts/GenerateHistoricalVerificationBatches.sh HistoryFull001
```

Este script crea lotes como `HistoryFull001-30d-critical`, `HistoryFull001-60d-warning` y
`HistoryFull001-90d-mixed`. Cada lote contiene muestras diarias por recurso y metrica para que
Grafana y VictoriaMetrics tengan datos historicos suficientes en paneles de tendencia,
percentil 95, forecast 30/60/90, saturacion y capacity planning.

En Grafana, usar el filtro `Lote`: `All` muestra todos los lotes y un lote especifico filtra todos
los cuadros SQL y series de VictoriaMetrics. En Zabbix se crean hosts sinteticos con items,
graficos por host y triggers Warning/Critical para validar alertamientos.

Para validar dashboards optimizados, usar un prefijo nuevo y revisar la carpeta `Capacity` en
Grafana:

```bash
Scripts/GenerateVerificationBatches.sh DashboardOpt001
Scripts/ManageTestData.sh validate --load-id DashboardOpt001-critical
```

Validar una serie sintetica en VictoriaMetrics:

```bash
curl "http://localhost:8428/api/v1/query?query=count_over_time%28synthetic_cpu%7Bload_id%3D%22DemoCritical001%22%7D%5B400d%5D%29"
```

## Uso de CapacityEngine

`CapacityEngine` es el motor Python que calcula KPIs de capacidad, forecast 30/60/90 dias, riesgo
de saturacion y recomendaciones. La implementacion actual ejecuta una corrida diaria deterministica
con datos de ejemplo internos para validar el flujo completo.

Ejecutar localmente desde la raiz del repositorio:

```bash
Scripts/RunCapacityDaily.sh
```

Salida esperada:

```text
Run-YYYYMMDDHHMMSS Succeeded resources=1
```

Ejecutar como modulo Python:

```bash
python3 -m CapacityEngine.Scheduler.DailyCapacityRun
```

Si el stack esta iniciado, consultar la ejecucion del contenedor:

```bash
Scripts/StackLogs.sh CapacityEngine 100
Scripts/StackStatus.sh CapacityEngine
```

`CapacityEngine` es una tarea batch: si termino con exit code `0`, el estado esperado es
`salud: completado correctamente`. No queda escuchando un puerto ni ejecutandose permanentemente.

Uso desde codigo Python:

```python
from CapacityEngine.Scheduler.DailyCapacityRun import RunDailyCapacity

Run = RunDailyCapacity()
print(Run.Status)
print(Run.Kpis)
print(Run.Forecasts)
print(Run.Risks)
print(Run.Recommendations)
```

La corrida devuelve un objeto `CapacityRun` con:

- `Kpis`: utilizacion promedio, pico, percentil 95, crecimiento mensual y headroom.
- `Forecasts`: proyecciones 30/60/90 dias y dias estimados hasta saturacion.
- `Risks`: riesgo por recurso segun umbrales.
- `Recommendations`: acciones recomendadas cuando existe riesgo relevante.

Para conectarlo a datos reales, el siguiente paso es reemplazar las muestras internas de
`CapacityEngine/Scheduler/DailyCapacityRun.py` por lecturas desde VictoriaMetrics y escritura de
resultados en PostgreSQL.

## Administracion de imagenes y stack

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
alcanza para reprovisionar dashboards sin reconstruir la imagen.

## Modo de uso

Con el stack iniciado, acceder desde el navegador o desde herramientas cliente:

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
servidor, por ejemplo `http://IP_DEL_SERVIDOR:3000`. En Oracle Cloud, AWS, Azure u otro proveedor,
abrir los puertos requeridos en el firewall del sistema operativo y en las reglas de red del
proveedor antes de acceder desde otra maquina.

PostgreSQL y Zabbix Server no son endpoints HTTP. No se validan con `curl`; se acceden con clientes
especificos o desde otros contenedores del stack.

Validar acceso local con los protocolos correctos:

```bash
Scripts/ValidateLocalAccess.sh
```

Para validar desde otro host o usando una IP/DNS:

```bash
Scripts/ValidateLocalAccess.sh IP_DEL_SERVIDOR
```

Interconexion interna del stack:

```text
Grafana -> capacity-performance-victoriametrics:8428
Grafana -> capacity-performance-postgresql:5432
ZabbixWeb -> capacity-performance-zabbix-server:10051
ZabbixWeb -> capacity-performance-postgresql:5432
ZabbixServer -> capacity-performance-postgresql:5432
ManageTestData -> PostgreSQL y VictoriaMetrics
CapacityEngine -> PostgreSQL y VictoriaMetrics
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

## Modo simulacion

Los scripts soportan `STACK_DRY_RUN=1` para validar comandos sin ejecutar Podman:

```bash
STACK_DRY_RUN=1 Scripts/BuildImages.sh Grafana v1.0.0
STACK_DRY_RUN=1 Scripts/StartStack.sh
STACK_DRY_RUN=1 Scripts/StackStatus.sh
STACK_DRY_RUN=1 Scripts/StackLogs.sh Grafana 50
STACK_DRY_RUN=1 Scripts/ValidateLocalAccess.sh
STACK_DRY_RUN=1 Scripts/StopStack.sh
STACK_DRY_RUN=1 Scripts/CleanupStack.sh --confirmar
```

## Validacion actual

La implementacion fue validada con:

```text
Scripts/RunTests.sh        -> 79 tests OK
Scripts/ValidateStack.sh   -> OK
STACK_DRY_RUN=1 build/start/status/logs/stop/cleanup -> OK
```

## Principios

El proyecto sigue la constitucion en `.specify/memory/constitution.md`:

- TDD obligatorio.
- SOLID y Clean Architecture.
- DRY y YAGNI.
- PascalCase para artefactos propios cuando la plataforma lo permite.
- Sin nuevas librerias externas ni servicios alojados.
- Validacion de entradas controladas por usuario.
- Rutas o acciones protegidas requieren autenticacion cuando aplican.

## Versionado

Version inicial publicada:

```text
v1.0.0
```

Repositorio:

```text
https://github.com/maferrara1961/Capacity_and_Performance
```
