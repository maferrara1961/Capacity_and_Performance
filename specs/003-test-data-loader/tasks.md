# Tasks: Datos de Prueba para Monitoreo, Performance y Capacity

**Input**: Design documents from `specs/003-test-data-loader/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/TestDataCli.md, quickstart.md

**Tests**: Mandatory by constitution. Test tasks are listed before implementation tasks for every user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare shared files and command entry points for the synthetic data feature.

- [X] T001 Create placeholder command wrapper in Scripts/ManageTestData.sh
- [X] T002 [P] Create Python command module placeholder in CapacityEngine/Scheduler/SyntheticDataCommand.py
- [X] T003 [P] Create synthetic domain module placeholder in CapacityEngine/Domain/SyntheticData.py
- [X] T004 [P] Create synthetic application service placeholder in CapacityEngine/Application/SyntheticDataService.py
- [X] T005 [P] Create PostgreSQL adapter placeholder in CapacityEngine/Adapters/SyntheticPostgreSqlAdapter.py
- [X] T006 [P] Create VictoriaMetrics adapter placeholder in CapacityEngine/Adapters/SyntheticVictoriaMetricsAdapter.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core contracts, validation boundaries, and schema support required before any story implementation.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T007 [P] Add contract tests for CLI actions and exit codes in Tests/Contract/SyntheticDataCliContractTest.py
- [X] T008 [P] Add unit tests for LoadId, profile, volume, days, seed, and delete confirmation validation in Tests/Unit/SyntheticDataValidationTest.py
- [X] T009 [P] Add unit tests for TestLoad state transitions and deletion rules in Tests/Unit/SyntheticDataValidationTest.py
- [X] T010 Add synthetic load tracking schema in Sql/Schema/003_TestDataLoads.sql
- [X] T011 Add test-data marker fields or companion mapping strategy in Sql/Schema/003_TestDataLoads.sql
- [X] T012 Implement core entities TestLoad, ToolValidationResult, and validation helpers in CapacityEngine/Domain/SyntheticData.py
- [X] T013 Implement CLI argument parsing and deterministic Spanish error handling in CapacityEngine/Scheduler/SyntheticDataCommand.py
- [X] T014 Implement shell wrapper validation and Python invocation in Scripts/ManageTestData.sh
- [X] T015 Add Scripts/ManageTestData.sh to Scripts/ValidateStack.sh required file validation
- [X] T016 Add docs command references for ManageTestData in README.md

**Checkpoint**: Foundation ready. CLI rejects invalid inputs, exposes actions, and schema support exists.

---

## Phase 3: User Story 1 - Cargar Datos de Prueba Representativos (Priority: P1) MVP

**Goal**: Generate one coherent synthetic dataset that validates dashboards and installed tools.

**Independent Test**: Execute a standard load and verify the summary includes generated services, resources, samples, KPIs, forecasts, risks, and recommendations.

### Tests for User Story 1

- [X] T017 [P] [US1] Add unit tests for scenario-based service/resource generation in Tests/Unit/SyntheticDataValidationTest.py
- [X] T018 [P] [US1] Add unit tests for metric sample ranges and trend shapes in Tests/Unit/SyntheticDataValidationTest.py
- [X] T019 [P] [US1] Add contract test for `Scripts/ManageTestData.sh load --profile mixed --volume small` summary in Tests/Contract/SyntheticDataCliContractTest.py
- [X] T020 [P] [US1] Add integration test for one successful synthetic load in Tests/Integration/SyntheticDataFlowTest.py

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement SyntheticService, SyntheticApplication, SyntheticResource, SyntheticMetricSample, SyntheticCapacityKpi, SyntheticForecast, SyntheticRisk, and SyntheticRecommendation entities in CapacityEngine/Domain/SyntheticData.py
- [X] T022 [US1] Implement scenario profile generation for normal, warning, critical, overprovisioned, underprovisioned, and mixed in CapacityEngine/Application/SyntheticDataService.py
- [X] T023 [US1] Implement deterministic random generation with optional seed in CapacityEngine/Application/SyntheticDataService.py
- [X] T024 [US1] Implement KPI, forecast, risk, and recommendation synthetic output creation in CapacityEngine/Application/SyntheticDataService.py
- [X] T025 [US1] Implement PostgreSQL write operations for catalog and capacity outputs in CapacityEngine/Adapters/SyntheticPostgreSqlAdapter.py
- [X] T026 [US1] Implement VictoriaMetrics import/write operation boundary for synthetic metric samples in CapacityEngine/Adapters/SyntheticVictoriaMetricsAdapter.py
- [X] T027 [US1] Wire `load` action orchestration in CapacityEngine/Scheduler/SyntheticDataCommand.py
- [X] T028 [US1] Print Spanish load summary with counts in CapacityEngine/Scheduler/SyntheticDataCommand.py

**Checkpoint**: User Story 1 is independently functional and demonstrable as the MVP.

---

## Phase 4: User Story 2 - Ejecutar Varias Cargas Independientes (Priority: P2)

**Goal**: Support multiple traceable loads without mixing executions.

**Independent Test**: Execute two loads with different identifiers and list both independently.

### Tests for User Story 2

- [X] T029 [P] [US2] Add contract tests for explicit and generated load ids in Tests/Contract/SyntheticDataCliContractTest.py
- [X] T030 [P] [US2] Add unit tests for duplicate LoadId rejection or safe unique generation in Tests/Unit/SyntheticDataValidationTest.py
- [X] T031 [P] [US2] Add integration test for two independent loads and list output in Tests/Integration/SyntheticDataFlowTest.py

### Implementation for User Story 2

- [X] T032 [US2] Implement TestLoad persistence, uniqueness checks, and status updates in CapacityEngine/Adapters/SyntheticPostgreSqlAdapter.py
- [X] T033 [US2] Implement generated LoadId behavior and duplicate handling in CapacityEngine/Application/SyntheticDataService.py
- [X] T034 [US2] Implement `list` action with status filtering in CapacityEngine/Scheduler/SyntheticDataCommand.py
- [X] T035 [US2] Ensure generated records carry LoadId and IsTestData marker in CapacityEngine/Application/SyntheticDataService.py
- [X] T036 [US2] Add multiple-load usage examples to README.md

**Checkpoint**: User Stories 1 and 2 work independently and together.

---

## Phase 5: User Story 3 - Borrar Datos de Prueba de Forma Controlada (Priority: P3)

**Goal**: Delete one load or all synthetic loads without affecting non-test data.

**Independent Test**: Load two datasets, delete one, verify the other remains, then delete all with confirmation.

### Tests for User Story 3

- [X] T037 [P] [US3] Add contract tests for delete by load id and delete all confirmation in Tests/Contract/SyntheticDataCliContractTest.py
- [X] T038 [P] [US3] Add unit tests for cleanup safety preserving non-test records in Tests/Unit/SyntheticDataValidationTest.py
- [X] T039 [P] [US3] Add integration test for selective cleanup and delete-all cleanup in Tests/Integration/SyntheticDataFlowTest.py

### Implementation for User Story 3

- [X] T040 [US3] Implement delete by LoadId in CapacityEngine/Adapters/SyntheticPostgreSqlAdapter.py
- [X] T041 [US3] Implement synthetic metric deletion by LoadId in CapacityEngine/Adapters/SyntheticVictoriaMetricsAdapter.py
- [X] T042 [US3] Implement delete-all guarded by `--confirmar` in CapacityEngine/Scheduler/SyntheticDataCommand.py
- [X] T043 [US3] Implement Spanish cleanup summary with deleted load and record counts in CapacityEngine/Scheduler/SyntheticDataCommand.py
- [X] T044 [US3] Add cleanup examples and safety warnings to README.md

**Checkpoint**: Synthetic data can be cleaned safely by load or all-test scope.

---

## Phase 6: User Story 4 - Validar Herramientas Instaladas con Datos Sinteticos (Priority: P4)

**Goal**: Validate installed tools and backing data after load/delete operations.

**Independent Test**: Run validation after a load and receive per-tool Spanish status; simulate a missing tool and receive deterministic failure.

### Tests for User Story 4

- [X] T045 [P] [US4] Add contract tests for `validate` action output per tool in Tests/Contract/SyntheticDataCliContractTest.py
- [X] T046 [P] [US4] Add integration test for validate after a synthetic load in Tests/Integration/SyntheticDataFlowTest.py
- [X] T047 [P] [US4] Add unit tests for ToolValidationResult statuses in Tests/Unit/SyntheticDataValidationTest.py

### Implementation for User Story 4

- [X] T048 [US4] Implement tool validation use case in CapacityEngine/Application/SyntheticDataService.py
- [X] T049 [US4] Implement PostgreSQL data presence validation in CapacityEngine/Adapters/SyntheticPostgreSqlAdapter.py
- [X] T050 [US4] Implement VictoriaMetrics data presence validation in CapacityEngine/Adapters/SyntheticVictoriaMetricsAdapter.py
- [X] T051 [US4] Wire `validate` action in CapacityEngine/Scheduler/SyntheticDataCommand.py
- [X] T052 [US4] Add validation examples to README.md and docs/AdministracionDeImagenes.md

**Checkpoint**: All user stories are independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and constitutional checks.

- [X] T053 [P] Update specs/003-test-data-loader/quickstart.md if implementation command behavior differs from contract
- [X] T054 [P] Add final operational documentation in docs/DatosDePruebaSinteticos.md
- [X] T055 Run Scripts/RunTests.sh and record updated test count in README.md
- [X] T056 Run Scripts/ValidateStack.sh and ensure no new dependency violations
- [X] T057 Run STACK_DRY_RUN=1 Scripts/ManageTestData.sh load --profile mixed --volume small
- [X] T058 Run STACK_DRY_RUN=1 Scripts/ManageTestData.sh delete --all --confirmar
- [X] T059 Verify no new external libraries, SDKs, packages, requirements files, or hosted services were introduced
- [X] T060 Verify project-defined Python symbols use PascalCase where runtime conventions allow it

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks all user stories.
- **Phase 3 US1**: Depends on Phase 2; MVP scope.
- **Phase 4 US2**: Depends on Phase 2 and can be built after or alongside US1, but full validation benefits from US1 load behavior.
- **Phase 5 US3**: Depends on Phase 2; safest after US1/US2 data creation exists.
- **Phase 6 US4**: Depends on Phase 2; practical validation depends on US1 data.
- **Phase 7 Polish**: Depends on implemented stories.

### User Story Dependencies

- **US1 (P1)**: MVP and first demonstrable increment.
- **US2 (P2)**: Independent load identity and listing; integrates with US1 generation.
- **US3 (P3)**: Independent cleanup; requires generated or mocked loads.
- **US4 (P4)**: Independent validation; strongest after US1 data exists.

### Parallel Opportunities

- T002-T006 can run in parallel after T001.
- T007-T009 can run in parallel before foundational implementation.
- T017-T020 can run in parallel for US1 tests.
- T029-T031 can run in parallel for US2 tests.
- T037-T039 can run in parallel for US3 tests.
- T045-T047 can run in parallel for US4 tests.
- T053-T054 can run in parallel during polish.

## Parallel Example: User Story 1

```text
Task: "T017 [P] [US1] Add unit tests for scenario-based service/resource generation in Tests/Unit/SyntheticDataValidationTest.py"
Task: "T018 [P] [US1] Add unit tests for metric sample ranges and trend shapes in Tests/Unit/SyntheticDataValidationTest.py"
Task: "T019 [P] [US1] Add contract test for `Scripts/ManageTestData.sh load --profile mixed --volume small` summary in Tests/Contract/SyntheticDataCliContractTest.py"
Task: "T020 [P] [US1] Add integration test for one successful synthetic load in Tests/Integration/SyntheticDataFlowTest.py"
```

## Parallel Example: User Story 2

```text
Task: "T029 [P] [US2] Add contract tests for explicit and generated load ids in Tests/Contract/SyntheticDataCliContractTest.py"
Task: "T030 [P] [US2] Add unit tests for duplicate LoadId rejection or safe unique generation in Tests/Unit/SyntheticDataValidationTest.py"
Task: "T031 [P] [US2] Add integration test for two independent loads and list output in Tests/Integration/SyntheticDataFlowTest.py"
```

## Parallel Example: User Story 3

```text
Task: "T037 [P] [US3] Add contract tests for delete by load id and delete all confirmation in Tests/Contract/SyntheticDataCliContractTest.py"
Task: "T038 [P] [US3] Add unit tests for cleanup safety preserving non-test records in Tests/Unit/SyntheticDataValidationTest.py"
Task: "T039 [P] [US3] Add integration test for selective cleanup and delete-all cleanup in Tests/Integration/SyntheticDataFlowTest.py"
```

## Parallel Example: User Story 4

```text
Task: "T045 [P] [US4] Add contract tests for `validate` action output per tool in Tests/Contract/SyntheticDataCliContractTest.py"
Task: "T046 [P] [US4] Add integration test for validate after a synthetic load in Tests/Integration/SyntheticDataFlowTest.py"
Task: "T047 [P] [US4] Add unit tests for ToolValidationResult statuses in Tests/Unit/SyntheticDataValidationTest.py"
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 setup.
2. Complete Phase 2 foundational contracts, validation, schema, and CLI boundary.
3. Complete Phase 3 US1.
4. Stop and validate one load independently using tests and quickstart.

### Incremental Delivery

1. US1: one representative load for dashboards.
2. US2: multiple loads and listing.
3. US3: cleanup by load and all-test cleanup.
4. US4: validation of installed tools and backing data.

### Format Validation

- All tasks use markdown checkbox format.
- All tasks have sequential IDs T001-T060.
- User story tasks include [US1], [US2], [US3], or [US4].
- Parallelizable tasks include [P].
- Every task includes an exact repository file path.
