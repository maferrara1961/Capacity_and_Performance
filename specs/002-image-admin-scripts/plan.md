# Plan de Implementacion: Scripts de Imagenes y Administracion

**Rama**: `002-image-admin-scripts` | **Fecha**: 2026-06-08 | **Spec**: [spec.md](./spec.md)

**Entrada**: Especificacion de feature desde `/specs/002-image-admin-scripts/spec.md`

## Resumen

Crear scripts operativos en castellano para construir imagenes, iniciar, detener, limpiar, consultar
logs y consultar estado del stack de capacidad y rendimiento. Los scripts deben respetar la
interconexion entre Zabbix, VictoriaMetrics, Grafana, PostgreSQL y CapacityEngine, validar entradas
del operador y reutilizar los artefactos existentes de `ContainerImages/`, `Config/PodmanStack.yml`
y `Config/StackManifest.yml`.

El enfoque tecnico separa reglas operativas de ejecucion concreta: la definicion de servicios,
dependencias, puertos, volumenes y nombres permitidos vive en una capa de configuracion/validacion;
los scripts consumen esa capa para ejecutar acciones sobre Podman sin duplicar logica.

## Contexto Tecnico

**Lenguaje/Version**: Shell POSIX compatible con Bash para scripts operativos; Python 3.11+ con
biblioteca estandar para pruebas auxiliares si hace falta.

**Dependencias Primarias**: Herramientas existentes del sistema y stack aprobado: Podman, shell,
Containerfiles ya definidos, `Config/PodmanStack.yml`, `Config/StackManifest.yml`. No se agregan
librerias externas, SDKs, paquetes ni servicios alojados.

**Almacenamiento**: Sin almacenamiento nuevo. Los scripts preservan volumenes persistentes definidos
para PostgreSQL, Grafana, VictoriaMetrics, Zabbix y CapacityEngine.

**Testing**: Shell smoke tests y `python3 -m unittest` usando biblioteca estandar. Las pruebas deben
validar comandos, mensajes en castellano, entradas invalidas, resolucion de raiz del repositorio y
contratos de interconexion.

**Plataforma Objetivo**: Linux y macOS con shell compatible y Podman disponible.

**Tipo de Proyecto**: Herramientas operativas CLI para administracion del stack local.

**Objetivos de Rendimiento**: `status` debe completar en menos de 30 segundos; `logs` debe devolver
salida del servicio solicitado con un solo comando; `build` debe reportar resumen final y detenerse
antes de construir si falta un artefacto requerido.

**Restricciones**: Toda salida para operador en castellano; validacion estricta de acciones y
servicios permitidos; no imprimir credenciales; stop no borra volumenes persistentes; cleanup
destructivo requiere accion explicita; simbolos propios en PascalCase cuando aplique.

**Escala/Alcance**: Scripts para build, start, stop, logs, status y cleanup sobre los servicios
Zabbix, VictoriaMetrics, Grafana, PostgreSQL y CapacityEngine.

## Chequeo de Constitucion

*GATE: Debe pasar antes de investigacion Phase 0. Revalidar despues de diseno Phase 1.*

- **TDD**: PASS. Las tareas deberan crear pruebas antes de modificar scripts para build, start,
  stop, logs, status, cleanup, validacion de entradas y dependencias.
- **SOLID / Clean Architecture**: PASS. Las reglas de servicios y validacion se separan de la
  ejecucion de comandos Podman.
- **DRY / YAGNI**: PASS. Una sola fuente de verdad define servicios permitidos, imagenes,
  contenedores, puertos, volumenes y dependencias; no se agregan abstracciones fuera del alcance.
- **PascalCase**: PASS con excepciones documentadas. Scripts shell, flags y nombres de contenedor
  pueden usar convenciones de plataforma.
- **Sin Nuevas Librerias Externas**: PASS. Se usan shell, Podman y biblioteca estandar.
- **Validacion y Auth**: PASS. No se agregan rutas protegidas. Todas las entradas de operador se
  validan antes de ejecutar acciones.

## Estructura del Proyecto

### Documentacion de esta feature

```text
specs/002-image-admin-scripts/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   |-- BuildContract.md
|   |-- LifecycleContract.md
|   `-- ObservabilityContract.md
`-- tasks.md
```

### Codigo fuente afectado

```text
Scripts/
|-- StackCommon.sh
|-- BuildImages.sh
|-- StartStack.sh
|-- StopStack.sh
|-- StackLogs.sh
|-- StackStatus.sh
|-- CleanupStack.sh
`-- ValidateStack.sh

Config/
|-- StackManifest.yml
`-- PodmanStack.yml

Tests/
|-- Contract/
|-- Integration/
`-- Unit/

docs/
`-- AdministracionDeImagenes.md
```

**Decision de Estructura**: Extender `Scripts/` con comandos dedicados y un archivo comun para
evitar duplicacion. Mantener `Config/StackManifest.yml` y `Config/PodmanStack.yml` como fuentes de
verdad para servicios e interconexion.

## Seguimiento de Complejidad

No hay violaciones de constitucion que requieran justificacion.

## Phase 0: Resumen de Investigacion

Las decisiones tecnicas estan consolidadas en [research.md](./research.md). No quedan aclaraciones
pendientes.

## Phase 1: Resumen de Diseno

El modelo de datos operativo esta en [data-model.md](./data-model.md). Los contratos estan en
[contracts/](./contracts/). La validacion end-to-end esta en [quickstart.md](./quickstart.md).

## Chequeo de Constitucion Posterior al Diseno

- **TDD**: PASS. Los contratos y quickstart definen escenarios verificables antes de implementar.
- **SOLID / Clean Architecture**: PASS. Las reglas operativas se mantienen separadas de comandos
  concretos.
- **DRY / YAGNI**: PASS. La planificacion se limita a scripts solicitados y fuente de verdad
  compartida.
- **PascalCase**: PASS con excepciones de shell y runtime documentadas.
- **Sin Nuevas Librerias Externas**: PASS. No se introducen dependencias nuevas.
- **Validacion y Auth**: PASS. Entradas y acciones destructivas estan cubiertas por validacion.
