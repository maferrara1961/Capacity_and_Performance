# Implementation Plan: Datos de Prueba para Monitoreo, Performance y Capacity

**Branch**: `003-test-data-loader` | **Date**: 2026-06-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-test-data-loader/spec.md`

## Summary

Crear un generador operativo de datos sinteticos para validar dashboards y herramientas del stack. El enfoque sera extender la arquitectura existente con dominio y casos de uso para cargas de prueba, un comando Python sin librerias externas, scripts de invocacion en castellano y contratos de CLI que permitan cargar, listar, validar y borrar lotes sin afectar datos no marcados como prueba.

## Technical Context

**Language/Version**: Python 3.11+ para el comando de carga y limpieza; Bash para wrappers operativos existentes.

**Primary Dependencies**: Solo libreria estandar de Python, Podman existente, `curl` existente para validaciones HTTP/TCP cuando aplique. No se agregan librerias externas.

**Storage**: PostgreSQL del stack para catalogo y resultados de capacity; VictoriaMetrics del stack para series de monitoreo/performance mediante endpoints existentes; archivos del repositorio solo para scripts, contratos y documentacion.

**Testing**: `Scripts/RunTests.sh` con `unittest` de Python, mas pruebas contract, integration y unit siguiendo la estructura `Tests/`.

**Target Platform**: Linux server con Podman, validado localmente y en Ubuntu/Oracle Linux.

**Project Type**: CLI/tooling operativo dentro de un stack de observabilidad self-hosted.

**Performance Goals**: Carga estandar completa en menos de 2 minutos en instancia pequena; limpieza por lote en menos de 1 minuto para volumen estandar.

**Constraints**: Sin nuevas dependencias; entradas validadas antes de escribir o borrar; borrado total requiere confirmacion explicita; mensajes en castellano; no eliminar datos sin marca de prueba.

**Scale/Scope**: Carga estandar orientada a demostracion y validacion: multiples servicios, recursos, series historicas, KPIs, forecasts, riesgos, recomendaciones y escenarios normal/warning/critical/over/under provisioned. Cargas mayores se habilitan por parametro validado.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **TDD**: PASS. El plan define pruebas unitarias para generacion/validacion, contract para CLI y summaries, e integracion para carga, listado, validacion y borrado.
- **SOLID / Clean Architecture**: PASS. Dominio sintetico independiente, casos de uso en aplicacion, adaptadores para PostgreSQL/VictoriaMetrics/comandos, wrappers en `Scripts/`.
- **DRY / YAGNI**: PASS. Reutiliza estructura existente; no introduce framework ni servicio nuevo; abstrae solo los puertos necesarios para persistencia y metricas.
- **PascalCase**: PASS. Simbolos Python de proyecto usaran PascalCase donde aplique; scripts mantienen convencion existente documentada.
- **No New External Libraries**: PASS. Solo libreria estandar y herramientas ya instaladas/aprobadas.
- **Validation and Auth**: PASS. Inputs CLI protegidos por validacion; delete-all requiere confirmacion; si luego se expone remotamente, debe requerir autenticacion.

## Project Structure

### Documentation (this feature)

```text
specs/003-test-data-loader/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── TestDataCli.md
└── tasks.md
```

### Source Code (repository root)

```text
CapacityEngine/
├── Application/
│   └── SyntheticDataService.py
├── Domain/
│   └── SyntheticData.py
├── Adapters/
│   ├── SyntheticPostgreSqlAdapter.py
│   └── SyntheticVictoriaMetricsAdapter.py
└── Scheduler/
    └── SyntheticDataCommand.py

Scripts/
└── ManageTestData.sh

Tests/
├── Unit/
│   └── SyntheticDataValidationTest.py
├── Contract/
│   └── SyntheticDataCliContractTest.py
└── Integration/
    └── SyntheticDataFlowTest.py
```

**Structure Decision**: Se extiende el proyecto existente de una sola base con capas `CapacityEngine/Domain`, `Application`, `Adapters`, `Scheduler`, scripts operativos y pruebas en `Tests/`. No se crea un nuevo paquete ni servicio.

## Complexity Tracking

No hay violaciones constitucionales que justificar.

## Phase 0: Research

Ver [research.md](research.md).

## Phase 1: Design & Contracts

- Modelo de datos: [data-model.md](data-model.md)
- Contrato CLI: [contracts/TestDataCli.md](contracts/TestDataCli.md)
- Guia de validacion: [quickstart.md](quickstart.md)

## Post-Design Constitution Check

- **TDD**: PASS. Los contratos y quickstart definen pruebas antes de implementar.
- **SOLID / Clean Architecture**: PASS. Entidades, servicios y adaptadores estan separados por responsabilidad.
- **DRY / YAGNI**: PASS. El diseno cubre solo carga/listado/validacion/borrado requeridos.
- **PascalCase**: PASS. Artefactos Python proyectados usan PascalCase; excepciones de scripts y SQL siguen convenciones existentes.
- **No New External Libraries**: PASS. El contrato prohibe dependencias nuevas.
- **Validation and Auth**: PASS. Entradas y delete-all quedan explicitamente protegidos por validacion/confirmacion.
