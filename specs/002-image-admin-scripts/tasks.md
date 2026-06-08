# Tareas: Scripts de Imagenes y Administracion

**Entrada**: Documentos de diseno desde `/specs/002-image-admin-scripts/`

**Prerequisitos**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Obligatorios por constitucion. Cada historia incluye pruebas antes de implementar.

**Organizacion**: Las tareas estan agrupadas por historia de usuario para permitir implementacion y
validacion independiente.

## Formato: `[ID] [P?] [Historia] Descripcion`

- **[P]**: Puede ejecutarse en paralelo porque toca archivos distintos
- **[Historia]**: Etiqueta de historia solo en fases de historias de usuario
- Todas las tareas incluyen rutas concretas

## Phase 1: Setup (Infraestructura Compartida)

**Proposito**: Preparar archivos comunes, documentacion y puntos de prueba para scripts operativos.

- [X] T001 Crear archivo comun de reglas operativas en Scripts/StackCommon.sh
- [X] T002 Crear script de build en Scripts/BuildImages.sh
- [X] T003 Crear script de logs en Scripts/StackLogs.sh
- [X] T004 Crear script de status en Scripts/StackStatus.sh
- [X] T005 Crear script de cleanup en Scripts/CleanupStack.sh
- [X] T006 Actualizar documentacion operativa base en docs/AdministracionDeImagenes.md
- [X] T007 [P] Crear archivo de pruebas unitarias para reglas comunes en Tests/Unit/StackCommonRulesTest.py
- [X] T008 [P] Crear archivo de pruebas contract para build en Tests/Contract/BuildImagesContractTest.py
- [X] T009 [P] Crear archivo de pruebas contract para ciclo de vida en Tests/Contract/LifecycleContractTest.py
- [X] T010 [P] Crear archivo de pruebas contract para logs y status en Tests/Contract/ObservabilityContractTest.py

---

## Phase 2: Foundational (Prerequisitos Bloqueantes)

**Proposito**: Centralizar servicios permitidos, validaciones, resolucion de raiz y mensajes en castellano.

**CRITICAL**: Ninguna historia puede implementarse hasta completar esta fase.

- [X] T011 Implementar resolucion de raiz del repositorio en Scripts/StackCommon.sh
- [X] T012 Implementar lista de servicios permitidos Zabbix, VictoriaMetrics, Grafana, PostgreSQL y CapacityEngine en Scripts/StackCommon.sh
- [X] T013 Implementar metadata de imagen, contenedor, Containerfile, puertos, volumenes y dependencias en Scripts/StackCommon.sh
- [X] T014 Implementar validacion de runtime Podman disponible en Scripts/StackCommon.sh
- [X] T015 Implementar validacion de servicio permitido en Scripts/StackCommon.sh
- [X] T016 Implementar validacion de version, cantidad de lineas y confirmacion destructiva en Scripts/StackCommon.sh
- [X] T017 Implementar helpers de mensajes y errores en castellano en Scripts/StackCommon.sh
- [X] T018 Implementar helpers de ejecucion simulable por variable `STACK_DRY_RUN` en Scripts/StackCommon.sh
- [X] T019 Actualizar Scripts/ValidateStack.sh para validar la presencia de los nuevos scripts operativos
- [X] T020 Crear pruebas unitarias para resolucion de raiz, servicios permitidos y entradas invalidas en Tests/Unit/StackCommonRulesTest.py

**Checkpoint**: Reglas compartidas listas para build, start, stop, logs, status y cleanup.

---

## Phase 3: Historia de Usuario 1 - Construir imagenes del stack (Prioridad: P1)

**Objetivo**: El operador puede construir todas las imagenes o una imagen individual con etiquetas
consistentes y mensajes en castellano.

**Prueba Independiente**: Ejecutar pruebas de contrato de build y validar que faltantes de
Containerfile, servicio invalido y version invalida fallan antes de construir.

### Tests para Historia de Usuario 1 (OBLIGATORIO - escribir antes de implementar)

- [X] T021 [P] [US1] Crear prueba fallida para build total con todos los Containerfiles en Tests/Contract/BuildImagesContractTest.py
- [X] T022 [P] [US1] Crear prueba fallida para build individual de Grafana en Tests/Contract/BuildImagesContractTest.py
- [X] T023 [P] [US1] Crear prueba fallida para rechazo de servicio invalido en build en Tests/Contract/BuildImagesContractTest.py
- [X] T024 [P] [US1] Crear prueba fallida para Containerfile faltante en build total en Tests/Contract/BuildImagesContractTest.py

### Implementacion para Historia de Usuario 1

- [X] T025 [US1] Implementar validacion previa de Containerfiles requeridos en Scripts/BuildImages.sh
- [X] T026 [US1] Implementar construccion de todas las imagenes con Podman en Scripts/BuildImages.sh
- [X] T027 [US1] Implementar construccion de una imagen individual por servicio en Scripts/BuildImages.sh
- [X] T028 [US1] Implementar etiquetas con proyecto, servicio y version en Scripts/BuildImages.sh
- [X] T029 [US1] Implementar resumen final de imagenes construidas o fallidas en Scripts/BuildImages.sh
- [X] T030 [US1] Documentar uso de build en docs/AdministracionDeImagenes.md

**Checkpoint**: Build completo e individual validado de forma independiente.

---

## Phase 4: Historia de Usuario 2 - Iniciar servicios interconectados (Prioridad: P2)

**Objetivo**: El operador puede iniciar el stack con red comun, dependencias, puertos, volumenes y
orden compatible con la interconexion.

**Prueba Independiente**: Ejecutar pruebas de start en modo dry-run y validar orden de servicios,
red comun, puertos y dependencias.

### Tests para Historia de Usuario 2 (OBLIGATORIO - escribir antes de implementar)

- [X] T031 [P] [US2] Crear prueba fallida para orden de arranque PostgreSQL y VictoriaMetrics antes de dependientes en Tests/Contract/LifecycleContractTest.py
- [X] T032 [P] [US2] Crear prueba fallida para creacion o reutilizacion de red comun en Tests/Contract/LifecycleContractTest.py
- [X] T033 [P] [US2] Crear prueba fallida para reporte de dependencia no saludable en Tests/Integration/StartStackFlowTest.py
- [X] T034 [P] [US2] Crear prueba fallida para mensajes de start en castellano en Tests/Integration/StartStackFlowTest.py

### Implementacion para Historia de Usuario 2

- [X] T035 [US2] Actualizar Scripts/StartStack.sh para cargar Scripts/StackCommon.sh
- [X] T036 [US2] Implementar creacion o reutilizacion de red comun en Scripts/StartStack.sh
- [X] T037 [US2] Implementar arranque ordenado por dependencias en Scripts/StartStack.sh
- [X] T038 [US2] Implementar configuracion de nombres, puertos y volumenes en Scripts/StartStack.sh
- [X] T039 [US2] Implementar chequeos basicos de salud posterior al arranque en Scripts/StartStack.sh
- [X] T040 [US2] Documentar interconexion y start en docs/AdministracionDeImagenes.md

**Checkpoint**: Start interconectado validado por dry-run y pruebas.

---

## Phase 5: Historia de Usuario 3 - Detener y limpiar servicios de forma segura (Prioridad: P3)

**Objetivo**: El operador puede detener el stack sin borrar datos y ejecutar limpieza explicita de
recursos temporales permitidos.

**Prueba Independiente**: Ejecutar pruebas de stop y cleanup en dry-run y verificar preservacion de
volumenes persistentes.

### Tests para Historia de Usuario 3 (OBLIGATORIO - escribir antes de implementar)

- [X] T041 [P] [US3] Crear prueba fallida para stop sin eliminar volumenes en Tests/Contract/LifecycleContractTest.py
- [X] T042 [P] [US3] Crear prueba fallida para cleanup sin confirmacion explicita en Tests/Contract/LifecycleContractTest.py
- [X] T043 [P] [US3] Crear prueba fallida para cleanup de recursos temporales permitidos en Tests/Integration/StopCleanupFlowTest.py

### Implementacion para Historia de Usuario 3

- [X] T044 [US3] Actualizar Scripts/StopStack.sh para cargar Scripts/StackCommon.sh
- [X] T045 [US3] Implementar detencion de contenedores administrados sin borrar volumenes en Scripts/StopStack.sh
- [X] T046 [US3] Implementar mensajes para servicios ya detenidos en Scripts/StopStack.sh
- [X] T047 [US3] Implementar confirmacion obligatoria `--confirmar` en Scripts/CleanupStack.sh
- [X] T048 [US3] Implementar limpieza de contenedores y red temporal permitida en Scripts/CleanupStack.sh
- [X] T049 [US3] Documentar stop y cleanup seguro en docs/AdministracionDeImagenes.md

**Checkpoint**: Stop y cleanup seguros validados.

---

## Phase 6: Historia de Usuario 4 - Consultar logs y estado operativo (Prioridad: P4)

**Objetivo**: El operador puede consultar logs y estado del stack completo o de un servicio
especifico con mensajes en castellano.

**Prueba Independiente**: Ejecutar logs y status en dry-run con servicio valido, servicio invalido y
cantidad de lineas invalida.

### Tests para Historia de Usuario 4 (OBLIGATORIO - escribir antes de implementar)

- [X] T050 [P] [US4] Crear prueba fallida para logs de servicio permitido en Tests/Contract/ObservabilityContractTest.py
- [X] T051 [P] [US4] Crear prueba fallida para rechazo de servicio inexistente en logs en Tests/Contract/ObservabilityContractTest.py
- [X] T052 [P] [US4] Crear prueba fallida para status de stack completo en Tests/Contract/ObservabilityContractTest.py
- [X] T053 [P] [US4] Crear prueba fallida para cantidad de lineas invalida en logs en Tests/Contract/ObservabilityContractTest.py

### Implementacion para Historia de Usuario 4

- [X] T054 [US4] Implementar logs de stack completo y por servicio en Scripts/StackLogs.sh
- [X] T055 [US4] Implementar validacion de cantidad de lineas en Scripts/StackLogs.sh
- [X] T056 [US4] Implementar status de stack completo y por servicio en Scripts/StackStatus.sh
- [X] T057 [US4] Implementar salida de puertos, red y salud basica en Scripts/StackStatus.sh
- [X] T058 [US4] Integrar StackLogs y StackStatus en Scripts/ValidateStack.sh
- [X] T059 [US4] Documentar logs y status en docs/AdministracionDeImagenes.md

**Checkpoint**: Logs y status validados de forma independiente.

---

## Phase 7: Pulido y Validacion Transversal

**Proposito**: Validar toda la feature, evitar duplicacion y dejar documentacion operativa completa.

- [X] T060 Ejecutar suite completa con Scripts/RunTests.sh
- [X] T061 Ejecutar validacion de stack con Scripts/ValidateStack.sh
- [X] T062 Ejecutar quickstart en modo dry-run y registrar resultado en specs/002-image-admin-scripts/quickstart.md
- [X] T063 Verificar que todos los mensajes nuevos de Scripts/ estan en castellano
- [X] T064 Verificar que no se agregaron librerias externas en Config/StackManifest.yml ni scripts
- [X] T065 Verificar convenciones PascalCase o documentar excepciones en docs/PascalCaseExceptions.md
- [X] T066 Revisar duplicacion entre Scripts/BuildImages.sh, Scripts/StartStack.sh, Scripts/StopStack.sh, Scripts/StackLogs.sh, Scripts/StackStatus.sh y Scripts/CleanupStack.sh

---

## Dependencias y Orden de Ejecucion

### Dependencias de Fase

- **Phase 1 Setup**: Sin dependencias.
- **Phase 2 Foundational**: Depende de Phase 1 y bloquea todas las historias.
- **Phase 3 US1**: Depende de Phase 2; MVP recomendado.
- **Phase 4 US2**: Depende de Phase 2 y requiere imagenes de US1 para ejecucion real.
- **Phase 5 US3**: Depende de Phase 2; puede validarse en dry-run.
- **Phase 6 US4**: Depende de Phase 2; puede validarse en dry-run.
- **Phase 7 Pulido**: Depende de las historias implementadas.

### Dependencias por Historia

- **US1 (P1)**: Crea build repetible y versionado de imagenes.
- **US2 (P2)**: Usa metadata comun y artefactos de imagen para start interconectado.
- **US3 (P3)**: Usa metadata comun para stop y cleanup seguro.
- **US4 (P4)**: Usa metadata comun para logs y status.

### Dentro de Cada Historia

- Las pruebas se escriben y fallan antes de implementar.
- Las reglas comunes preceden a scripts especificos.
- La documentacion se actualiza al cierre de cada historia.
- Cada checkpoint debe pasar antes de avanzar en entrega secuencial.

## Oportunidades de Paralelismo

- T007-T010 pueden crearse en paralelo.
- T011-T018 deben coordinarse porque tocan Scripts/StackCommon.sh.
- Pruebas contract dentro de cada historia pueden escribirse en paralelo.
- Documentacion de cada historia puede avanzar despues de que su script este definido.

## Ejemplo Paralelo: Historia de Usuario 1

```bash
Task: "Crear prueba fallida para build total con todos los Containerfiles en Tests/Contract/BuildImagesContractTest.py"
Task: "Crear prueba fallida para build individual de Grafana en Tests/Contract/BuildImagesContractTest.py"
Task: "Crear prueba fallida para rechazo de servicio invalido en build en Tests/Contract/BuildImagesContractTest.py"
```

## Ejemplo Paralelo: Historia de Usuario 4

```bash
Task: "Crear prueba fallida para logs de servicio permitido en Tests/Contract/ObservabilityContractTest.py"
Task: "Crear prueba fallida para status de stack completo en Tests/Contract/ObservabilityContractTest.py"
```

## Estrategia de Implementacion

### MVP Primero (Solo Historia de Usuario 1)

1. Completar Phase 1.
2. Completar Phase 2.
3. Completar US1.
4. Validar build total e individual.

### Entrega Incremental

1. US1: build de imagenes.
2. US2: start interconectado.
3. US3: stop y cleanup seguro.
4. US4: logs y status.
5. Pulido y validacion completa.

## Resumen

- Total de tareas: 66
- Setup: 10
- Foundational: 10
- US1: 10
- US2: 10
- US3: 9
- US4: 10
- Pulido: 7
- MVP sugerido: Phase 1 + Phase 2 + US1
