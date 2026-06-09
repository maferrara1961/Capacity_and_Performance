# Capacity and Performance

Stack self-hosted para monitoreo tecnico, observabilidad de capacidad y administracion operativa de
imagenes con Podman, Zabbix, VictoriaMetrics, Grafana, PostgreSQL y un motor de capacidad en Python.

El objetivo es ofrecer una arquitectura moderna, escalable y sin costos de licencias para visualizar
estado operativo, capacidad usada, riesgo de saturacion, forecast, top consumidores y relacion entre
servicios, aplicaciones e infraestructura.

## Componentes

- **Zabbix**: monitoreo de sistemas y subsistemas.
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
STACK_DRY_RUN=1 Scripts/StopStack.sh
STACK_DRY_RUN=1 Scripts/CleanupStack.sh --confirmar
```

## Validacion actual

La implementacion fue validada con:

```text
Scripts/RunTests.sh        -> 37 tests OK
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
