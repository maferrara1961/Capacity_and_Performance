# Tareas: Plataforma Enterprise de Gobierno

**Input**: Documentos de diseno desde `specs/005-enterprise-governance-platform/`

**Prerequisitos**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Obligatorios por constitucion. Cada historia incluye pruebas antes de implementacion.

**Organizacion**: Las tareas estan agrupadas por historia para permitir implementacion y validacion independiente.

## Phase 1: Setup (Infraestructura Compartida)

**Proposito**: Preparar estructura, validaciones y documentacion base para el feature enterprise.

- [X] T001 Crear documento de arquitectura enterprise en `docs/EnterpriseGovernancePlatform.md`
- [X] T002 [P] Crear contrato de excepciones PascalCase enterprise en `docs/PascalCaseExceptions.md`
- [X] T003 [P] Agregar referencias del feature enterprise en `README.md`
- [X] T004 [P] Crear prueba contract de documentacion enterprise en `Tests/Contract/EnterpriseGovernanceDocumentationContractTest.py`
- [X] T005 Ejecutar `Scripts/RunTests.sh` y confirmar que la prueba contract nueva falla por falta de contenido enterprise

---

## Phase 2: Foundational (Prerequisitos Bloqueantes)

**Proposito**: Crear el modelo de dominio compartido y las reglas base que bloquean todas las historias.

**CRITICO**: Ninguna historia debe implementarse antes de completar esta fase.

- [X] T006 [P] Crear pruebas unitarias para `TechnologyDomain`, `TechnologyComponent`, `BusinessService` y `ServiceComponentMap` en `Tests/Unit/EnterpriseInventoryValidationTest.py`
- [X] T007 [P] Crear pruebas unitarias para `EvidenceRecord`, `EvidenceState` y reglas de evidencia faltante en `Tests/Unit/EnterpriseEvidenceValidationTest.py`
- [X] T008 [P] Crear pruebas unitarias para `ScoreAssessment`, `RiskAssessment`, `RiskRegistryEntry`, `Recommendation` y `ForecastResult` en `Tests/Unit/EnterpriseAssessmentValidationTest.py`
- [X] T009 Crear entidades enterprise en `CapacityEngine/Domain/EnterpriseEntities.py`
- [X] T010 Crear constantes enterprise de dominios, estados, severidades, scores y clasificaciones en `CapacityEngine/Domain/EnterpriseConstants.py`
- [X] T011 Crear validadores enterprise sin librerias externas en `CapacityEngine/Domain/EnterpriseValidators.py`
- [X] T012 Crear puertos de aplicacion enterprise en `CapacityEngine/Application/EnterprisePorts.py`
- [X] T013 Actualizar exports de dominio en `CapacityEngine/Domain/__init__.py`
- [X] T014 Actualizar exports de aplicacion en `CapacityEngine/Application/__init__.py`
- [X] T015 Ejecutar `Scripts/RunTests.sh` y confirmar que las pruebas foundational pasan

---

## Phase 3: Historia de Usuario 1 - Vista Ejecutiva de Salud Tecnologica (Prioridad: P1)

**Objetivo**: Entregar vista ejecutiva con Technology Health Score, scores por dominio, confianza de monitoreo, top riesgos y recomendaciones accionables.

**Prueba independiente**: Cargar evidencia representativa y confirmar que un ejecutivo identifica salud actual, riesgos principales, servicios afectados, tendencias y prioridades sin acceder a sistemas fuente.

### Pruebas para US1 (escribir antes de implementar)

- [X] T016 [P] [US1] Crear pruebas unitarias de scoring 0-100 y clasificacion 90/75/60/40 en `Tests/Unit/EnterpriseScoringTest.py`
- [X] T017 [P] [US1] Crear pruebas unitarias de no inferir Healthy desde evidencia faltante en `Tests/Unit/EnterpriseScoringTest.py`
- [X] T018 [P] [US1] Crear prueba contract para paneles ejecutivos enterprise en `Tests/Contract/EnterpriseExecutiveDashboardContractTest.py`
- [X] T019 [P] [US1] Crear prueba contract para dataset de score y top riesgos en `Tests/Contract/EnterpriseDatasetContractTest.py`
- [X] T020 [US1] Ejecutar `Scripts/RunTests.sh` y confirmar fallas esperadas de US1

### Implementacion para US1

- [X] T021 [P] [US1] Implementar calculadora de scores enterprise en `CapacityEngine/Application/EnterpriseScoringService.py`
- [X] T022 [P] [US1] Implementar servicio de registro de riesgos enterprise en `CapacityEngine/Application/EnterpriseRiskRegistryService.py`
- [X] T023 [US1] Implementar servicio de evaluacion Technology Health Score en `CapacityEngine/Application/EnterpriseAssessmentService.py`
- [X] T024 [US1] Extender SQL de PostgreSQL enterprise para scores, riesgos y recomendaciones en `CapacityEngine/Adapters/SyntheticPostgreSqlAdapter.py`
- [X] T025 [US1] Crear dashboard ejecutivo enterprise provisionado en `Config/Grafana/Dashboards/EnterpriseExecutiveDashboard.json`
- [X] T026 [US1] Registrar dashboard ejecutivo enterprise en `Config/Grafana/DashboardProviders/Provisioning.yml`
- [X] T027 [US1] Agregar datos sinteticos enterprise de score/riesgo/recomendacion en `CapacityEngine/Application/SyntheticDataService.py`
- [X] T028 [US1] Actualizar validacion de dashboards enterprise en `Scripts/ValidateStack.sh`
- [X] T029 [US1] Ejecutar `Scripts/RunTests.sh` y confirmar que US1 pasa de forma independiente

---

## Phase 4: Historia de Usuario 2 - Gobierno por Servicio y Dominio (Prioridad: P2)

**Objetivo**: Entregar inventario tecnologico, mapeo servicio-componente, ciclo de vida, cumplimiento, confianza de monitoreo y registro de riesgos gobernable.

**Prueba independiente**: Cargar inventario y evidencia de riesgo para multiples servicios/dominios y confirmar que cada riesgo, score y recomendacion identifica tecnologias, servicios, owners, ciclo de vida, cumplimiento y evidencia.

### Pruebas para US2 (escribir antes de implementar)

- [X] T030 [P] [US2] Crear pruebas unitarias de inventario y mapeo servicio-componente en `Tests/Unit/EnterpriseInventoryServiceTest.py`
- [X] T031 [P] [US2] Crear pruebas unitarias de lifecycle/compliance/monitoring confidence en `Tests/Unit/EnterpriseGovernanceAssessmentTest.py`
- [X] T032 [P] [US2] Crear prueba contract para CLI enterprise en `Tests/Contract/EnterpriseCliContractTest.py`
- [X] T033 [P] [US2] Crear prueba contract para dashboard de gobierno en `Tests/Contract/EnterpriseGovernanceDashboardContractTest.py`
- [X] T034 [US2] Ejecutar `Scripts/RunTests.sh` y confirmar fallas esperadas de US2

### Implementacion para US2

- [X] T035 [P] [US2] Implementar servicio de inventario enterprise en `CapacityEngine/Application/EnterpriseInventoryService.py`
- [X] T036 [P] [US2] Implementar servicio de lifecycle y compliance en `CapacityEngine/Application/EnterpriseGovernanceService.py`
- [X] T037 [US2] Implementar sincronizacion de inventario enterprise con Zabbix en `CapacityEngine/Adapters/SyntheticZabbixAdapter.py`
- [X] T038 [US2] Crear comando `sync-enterprise-inventory` en `CapacityEngine/Scheduler/SyntheticDataCommand.py`
- [X] T039 [US2] Crear script `Scripts/RunEnterpriseAssessment.sh`
- [X] T040 [US2] Crear script `Scripts/ValidateEnterpriseGovernance.sh`
- [X] T041 [US2] Crear dashboard de gobierno enterprise en `Config/Grafana/Dashboards/EnterpriseGovernanceDashboard.json`
- [X] T042 [US2] Registrar dashboard de gobierno enterprise en `Config/Grafana/DashboardProviders/Provisioning.yml`
- [X] T043 [US2] Documentar uso de gobierno enterprise en `docs/EnterpriseGovernancePlatform.md`
- [X] T044 [US2] Ejecutar `Scripts/RunTests.sh` y confirmar que US2 pasa de forma independiente

---

## Phase 5: Historia de Usuario 3 - Analisis Operativo y de Tendencias (Prioridad: P3)

**Objetivo**: Entregar dashboards operativos, tendencias historicas, forecasts 30/90/180/365, top consumidores, saturacion y frescura de evidencia.

**Prueba independiente**: Cargar telemetria historica y confirmar que vistas operativas muestran capacidad, performance, disponibilidad, estacionalidad, crecimiento, horizontes de forecast, top consumidores y frescura.

### Pruebas para US3 (escribir antes de implementar)

- [X] T045 [P] [US3] Crear pruebas unitarias de forecast 30/90/180/365 con evidencia suficiente e insuficiente en `Tests/Unit/EnterpriseForecastTest.py`
- [X] T046 [P] [US3] Crear pruebas unitarias de frescura de evidencia y confianza de monitoreo en `Tests/Unit/EnterpriseEvidenceFreshnessTest.py`
- [X] T047 [P] [US3] Crear prueba contract para dashboard operativo enterprise en `Tests/Contract/EnterpriseOperationalDashboardContractTest.py`
- [X] T048 [P] [US3] Crear prueba integration de carga historica enterprise en `Tests/Integration/EnterpriseOperationalFlowTest.py`
- [X] T049 [US3] Ejecutar `Scripts/RunTests.sh` y confirmar fallas esperadas de US3

### Implementacion para US3

- [X] T050 [P] [US3] Implementar servicio de forecast enterprise en `CapacityEngine/Application/EnterpriseForecastService.py`
- [X] T051 [P] [US3] Implementar servicio de frescura de evidencia en `CapacityEngine/Application/EnterpriseEvidenceService.py`
- [X] T052 [US3] Extender publicacion VictoriaMetrics con labels enterprise en `CapacityEngine/Adapters/SyntheticVictoriaMetricsAdapter.py`
- [X] T053 [US3] Crear generador de datos enterprise historicos en `CapacityEngine/Application/SyntheticDataService.py`
- [X] T054 [US3] Crear comando de generacion enterprise en `CapacityEngine/Scheduler/SyntheticDataCommand.py`
- [X] T055 [US3] Crear script `Scripts/GenerateEnterpriseVerificationData.sh`
- [X] T056 [US3] Crear dashboard operativo enterprise en `Config/Grafana/Dashboards/EnterpriseOperationalDashboard.json`
- [X] T057 [US3] Registrar dashboard operativo enterprise en `Config/Grafana/DashboardProviders/Provisioning.yml`
- [X] T058 [US3] Actualizar quickstart operativo en `docs/EnterpriseGovernancePlatform.md`
- [X] T059 [US3] Ejecutar `Scripts/RunTests.sh` y confirmar que US3 pasa de forma independiente

---

## Phase 6: Pulido y Transversales

**Proposito**: Validar consistencia final, documentacion, seguridad y ausencia de regresiones.

- [X] T060 [P] Actualizar `README.md` con comandos enterprise y dashboards nuevos
- [X] T061 [P] Actualizar `ARCH.md` con subsistema enterprise, flujos y datasets nuevos
- [X] T062 [P] Actualizar `docs/DatosDePruebaSinteticos.md` con cargas enterprise
- [X] T063 Verificar que no se agregaron librerias externas en `ContainerImages/CapacityEngine/Containerfile`
- [X] T064 Verificar excepciones PascalCase documentadas en `docs/PascalCaseExceptions.md`
- [X] T065 Ejecutar `Scripts/ValidateStack.sh`
- [X] T066 Ejecutar `Scripts/RunTests.sh`
- [X] T067 Ejecutar dry-run de comandos enterprise con `STACK_DRY_RUN=1`
- [X] T068 Revisar que dashboards muestren evidencia faltante como faltante y no como saludable en `Config/Grafana/Dashboards/`
- [X] T069 Actualizar versionado y notas de uso en `README.md`

---

## Dependencias y Orden de Ejecucion

### Dependencias de Fase

- **Phase 1 Setup**: sin dependencias.
- **Phase 2 Foundational**: depende de Phase 1 y bloquea todas las historias.
- **US1 P1**: depende de Phase 2. Es el MVP.
- **US2 P2**: depende de Phase 2 y puede avanzar despues de US1 si comparte scoring/riesgo.
- **US3 P3**: depende de Phase 2 y puede avanzar en paralelo con US2 si no modifica los mismos archivos.
- **Phase 6 Pulido**: depende de US1, US2 y US3.

### Dependencias por Historia

- **US1** entrega scoring, Technology Health Score, riesgos y dashboard ejecutivo.
- **US2** reutiliza entidades, evidencia, scoring y riesgos para inventario, lifecycle, compliance y gobierno.
- **US3** reutiliza entidades y evidencia para forecast, tendencias y dashboard operativo.

### Orden Interno

- Pruebas antes de implementacion en cada historia.
- Entidades y validadores antes de servicios.
- Servicios antes de adapters/scripts.
- Adapters/scripts antes de dashboards y validaciones end-to-end.

## Oportunidades de Paralelismo

- T002, T003 y T004 pueden ejecutarse en paralelo.
- T006, T007 y T008 pueden ejecutarse en paralelo.
- T016, T017, T018 y T019 pueden ejecutarse en paralelo.
- T021 y T022 pueden ejecutarse en paralelo.
- T030, T031, T032 y T033 pueden ejecutarse en paralelo.
- T035 y T036 pueden ejecutarse en paralelo.
- T045, T046, T047 y T048 pueden ejecutarse en paralelo.
- T050 y T051 pueden ejecutarse en paralelo.
- T060, T061 y T062 pueden ejecutarse en paralelo.

## Ejemplos de Ejecucion Paralela

### US1

```text
T016 EnterpriseScoringTest
T017 no inferir Healthy desde evidencia faltante
T018 EnterpriseExecutiveDashboardContractTest
T019 EnterpriseDatasetContractTest
```

### US2

```text
T030 EnterpriseInventoryServiceTest
T031 EnterpriseGovernanceAssessmentTest
T032 EnterpriseCliContractTest
T033 EnterpriseGovernanceDashboardContractTest
```

### US3

```text
T045 EnterpriseForecastTest
T046 EnterpriseEvidenceFreshnessTest
T047 EnterpriseOperationalDashboardContractTest
T048 EnterpriseOperationalFlowTest
```

## Estrategia de Implementacion

### MVP Primero

1. Completar Phase 1 Setup.
2. Completar Phase 2 Foundational.
3. Implementar US1 completa.
4. Validar dashboard ejecutivo, scores, top riesgos y evidencia faltante.
5. Publicar como incremento MVP.

### Entrega Incremental

1. US1: vista ejecutiva y scoring.
2. US2: gobierno, inventario, lifecycle, compliance y registro de riesgos.
3. US3: tendencias, forecast y vistas operativas.
4. Pulido final con documentacion, validacion stack y versionado.

## Resumen de Conteo

- Total de tareas: 69
- Setup: 5
- Foundational: 10
- US1: 14
- US2: 15
- US3: 15
- Pulido: 10
- Tareas paralelizables marcadas: 24
- Alcance MVP sugerido: Phase 1 + Phase 2 + US1
