# Tasks: Grafana Dashboard Optimization

**Input**: Design documents from `specs/004-grafana-dashboard-optimization/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: Tests are mandatory by constitution. Write failing contract/integration tests before implementation tasks for every user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files or has no dependency on incomplete tasks
- **[Story]**: User story label, only for user story phases
- Every task includes an exact repository path

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the dashboard optimization baseline and protect the Grafana provisioning path.

- [ ] T001 Inspect current dashboard panel inventory and document gaps against `specs/004-grafana-dashboard-optimization/contracts/DashboardCatalogContract.md` in `specs/004-grafana-dashboard-optimization/research.md`
- [ ] T002 Verify Grafana datasource provisioning remains idempotent and repository-mounted in `Config/Grafana/Datasources/Datasources.yml`
- [ ] T003 [P] Verify dashboard provider path separation in `Config/Grafana/DashboardProviders/Provisioning.yml`
- [ ] T004 [P] Verify no new external dependencies are needed by checking `ContainerImages/Grafana/Containerfile` and `Scripts/StackCommon.sh`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add shared validation coverage and reusable dashboard expectations before story-specific changes.

**Critical**: No user story implementation should begin until this phase is complete.

- [ ] T005 [P] Add shared dashboard JSON loading helpers for contract tests in `Tests/Contract/GrafanaDatasourceContractTest.py`
- [ ] T006 [P] Add required KPI coverage assertions for average, peak, P95, growth, headroom, forecast, days-to-saturation, and baseline in `Tests/Contract/GrafanaDatasourceContractTest.py`
- [ ] T007 [P] Add verification scenario profile coverage assertions for normal, warning, critical, and mixed in `Tests/Contract/SyntheticDataCliContractTest.py`
- [ ] T008 Add stack validation checks for optimized dashboard files and provider paths in `Scripts/ValidateStack.sh`
- [ ] T009 Add documentation placeholder for optimized dashboard usage in `docs/DatosDePruebaSinteticos.md`

**Checkpoint**: Foundation ready; user story phases can proceed.

---

## Phase 3: User Story 1 - Decision Capacity Overview (Priority: P1) MVP

**Goal**: Deliver executive capacity dashboards that surface risk, forecast, headroom, and recommended actions for decision making.

**Independent Test**: Load representative critical data and verify the executive dashboard exposes overall state, top risks, 30/60/90 forecast, headroom, and recommendations without requiring raw metric inspection.

### Tests for User Story 1

- [ ] T010 [P] [US1] Add executive dashboard contract tests for overall state, top risk, forecast, headroom, and recommendations in `Tests/Contract/ExecutiveDashboardContractTest.py`
- [ ] T011 [P] [US1] Add executive dashboard integration expectations for critical verification data in `Tests/Integration/ExecutiveCapacityFlowTest.py`
- [ ] T012 [P] [US1] Add executive panel purpose assertions against `contracts/DashboardCatalogContract.md` in `Tests/Contract/ExecutiveDashboardContractTest.py`

### Implementation for User Story 1

- [ ] T013 [US1] Redesign executive stat and summary panels in `Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json`
- [ ] T014 [US1] Add top 5 capacity risk and recommendation table coverage in `Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json`
- [ ] T015 [US1] Add forecast 30/60/90 and days-to-saturation decision panels in `Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json`
- [ ] T016 [US1] Add used capacity versus headroom summary panels in `Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json`
- [ ] T017 [US1] Ensure executive dashboard panel titles and descriptions distinguish missing data from OK state in `Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json`
- [ ] T018 [US1] Validate executive dashboard with `Scripts/RunTests.sh` and document expected manual validation in `specs/004-grafana-dashboard-optimization/quickstart.md`

**Checkpoint**: User Story 1 is independently testable and provides the MVP.

---

## Phase 4: User Story 2 - Technical Performance Diagnosis (Priority: P2)

**Goal**: Deliver technical dashboards that expose metric-level performance diagnosis for operational improvement.

**Independent Test**: Load representative warning or mixed data and verify technical panels expose CPU, memory, storage, IOPS, network, latency, throughput, errors, saturation, resource context, and severity.

### Tests for User Story 2

- [ ] T019 [P] [US2] Add technical metric coverage tests for CPU, RAM, storage, IOPS, network, latency, throughput, errors, and saturation in `Tests/Contract/TechnicalDashboardContractTest.py`
- [ ] T020 [P] [US2] Add technical integration expectations for warning and mixed verification data in `Tests/Integration/TechnicalPerformanceFlowTest.py`
- [ ] T021 [P] [US2] Add top consumer and outlier panel assertions in `Tests/Contract/TechnicalDashboardContractTest.py`

### Implementation for User Story 2

- [ ] T022 [US2] Redesign technical compute and memory panels in `Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json`
- [ ] T023 [US2] Redesign storage, IOPS, and network panels in `Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json`
- [ ] T024 [US2] Add latency, throughput, errors, and saturation diagnostic panels in `Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json`
- [ ] T025 [US2] Add top consumer and outlier tables with service and resource context in `Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json`
- [ ] T026 [US2] Ensure technical dashboard panel titles and legends expose resource, service, metric, and severity context in `Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json`
- [ ] T027 [US2] Validate technical dashboard with `Scripts/RunTests.sh` and update expected validation in `specs/004-grafana-dashboard-optimization/quickstart.md`

**Checkpoint**: User Story 2 is independently testable and does not require executive dashboard changes beyond shared data.

---

## Phase 5: User Story 3 - Service-Oriented Capacity Planning (Priority: P3)

**Goal**: Deliver planning and application dashboards that connect infrastructure trends to services and classify overprovisioned and underprovisioned resources.

**Independent Test**: Load representative mixed data and verify planning/application dashboards show service mapping, growth, headroom, baseline comparison, days to saturation, sizing categories, and dependencies.

### Tests for User Story 3

- [ ] T028 [P] [US3] Add planning dashboard contract tests for growth, headroom, baseline, forecast, and days-to-saturation in `Tests/Contract/CapacityPlanningDashboardContractTest.py`
- [ ] T029 [P] [US3] Add application/service context contract tests for health, infrastructure, dependencies, and end-to-end performance in `Tests/Contract/ApplicationDashboardContractTest.py`
- [ ] T030 [P] [US3] Add capacity planning integration expectations for mixed verification data in `Tests/Integration/CapacityPlanningFlowTest.py`

### Implementation for User Story 3

- [ ] T031 [US3] Redesign capacity planning growth and headroom sections in `Config/Grafana/Dashboards/CapacityPlanningDashboard.json`
- [ ] T032 [US3] Add overprovisioned and underprovisioned resource classification panels in `Config/Grafana/Dashboards/CapacityPlanningDashboard.json`
- [ ] T033 [US3] Add baseline comparison and days-to-saturation planning panels in `Config/Grafana/Dashboards/CapacityPlanningDashboard.json`
- [ ] T034 [US3] Redesign application health and associated infrastructure sections in `Config/Grafana/Dashboards/ApplicationDashboard.json`
- [ ] T035 [US3] Add critical dependency and end-to-end performance context panels in `Config/Grafana/Dashboards/ApplicationDashboard.json`
- [ ] T036 [US3] Validate planning and application dashboards with `Scripts/RunTests.sh` and update expected validation in `specs/004-grafana-dashboard-optimization/quickstart.md`

**Checkpoint**: User Story 3 is independently testable and adds service-oriented planning value.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate end-to-end behavior, documentation, and constitutional constraints.

- [ ] T037 [P] Update dashboard usage documentation in `README.md`
- [ ] T038 [P] Update dashboard administration instructions in `docs/AdministracionDeImagenes.md`
- [ ] T039 [P] Update synthetic data validation guidance in `docs/DatosDePruebaSinteticos.md`
- [ ] T040 Run `Scripts/RunTests.sh` and fix any dashboard contract or integration failures
- [ ] T041 Run `Scripts/ValidateStack.sh` and fix any provisioning validation failures
- [ ] T042 Run `STACK_DRY_RUN=1 Scripts/StartStack.sh` and confirm Grafana mounts datasource, provider, and dashboard paths
- [ ] T043 Execute quickstart validation from `specs/004-grafana-dashboard-optimization/quickstart.md` on a real stack
- [ ] T044 Verify no new external libraries, SDKs, packages, hosted services, or licensed products were introduced in `ContainerImages/`, `CapacityEngine/`, and `Scripts/`
- [ ] T045 Verify project-defined symbols and artifacts keep PascalCase or documented external schema exceptions in `docs/PascalCaseExceptions.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; can start immediately.
- **Phase 2 Foundational**: Depends on Phase 1; blocks all user stories.
- **Phase 3 US1**: Depends on Phase 2; MVP delivery.
- **Phase 4 US2**: Depends on Phase 2; can run after or in parallel with US1, but final polish should validate both together.
- **Phase 5 US3**: Depends on Phase 2; can run after or in parallel with US1/US2, but depends on shared service mapping assumptions.
- **Phase 6 Polish**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 Decision Capacity Overview**: No dependency on US2 or US3 after foundation; recommended MVP.
- **US2 Technical Performance Diagnosis**: No dependency on US1 after foundation; shares verification data and datasource assumptions.
- **US3 Service-Oriented Capacity Planning**: No dependency on US1/US2 after foundation; shares service context and verification data.

### Within Each User Story

- Tests must be written first and confirmed failing for the expected reason.
- Dashboard JSON implementation follows the failing tests.
- Quickstart/documentation updates follow successful story validation.

## Parallel Opportunities

- T003 and T004 can run in parallel during setup.
- T005, T006, and T007 can run in parallel during foundation.
- US1 tests T010, T011, and T012 can run in parallel.
- US2 tests T019, T020, and T021 can run in parallel.
- US3 tests T028, T029, and T030 can run in parallel.
- Documentation tasks T037, T038, and T039 can run in parallel after story implementation.

## Parallel Example: User Story 1

```text
Task: "T010 [P] [US1] Add executive dashboard contract tests for overall state, top risk, forecast, headroom, and recommendations in Tests/Contract/ExecutiveDashboardContractTest.py"
Task: "T011 [P] [US1] Add executive dashboard integration expectations for critical verification data in Tests/Integration/ExecutiveCapacityFlowTest.py"
Task: "T012 [P] [US1] Add executive panel purpose assertions against contracts/DashboardCatalogContract.md in Tests/Contract/ExecutiveDashboardContractTest.py"
```

## Parallel Example: User Story 2

```text
Task: "T019 [P] [US2] Add technical metric coverage tests for CPU, RAM, storage, IOPS, network, latency, throughput, errors, and saturation in Tests/Contract/TechnicalDashboardContractTest.py"
Task: "T020 [P] [US2] Add technical integration expectations for warning and mixed verification data in Tests/Integration/TechnicalPerformanceFlowTest.py"
Task: "T021 [P] [US2] Add top consumer and outlier panel assertions in Tests/Contract/TechnicalDashboardContractTest.py"
```

## Parallel Example: User Story 3

```text
Task: "T028 [P] [US3] Add planning dashboard contract tests for growth, headroom, baseline, forecast, and days-to-saturation in Tests/Contract/CapacityPlanningDashboardContractTest.py"
Task: "T029 [P] [US3] Add application/service context contract tests for health, infrastructure, dependencies, and end-to-end performance in Tests/Contract/ApplicationDashboardContractTest.py"
Task: "T030 [P] [US3] Add capacity planning integration expectations for mixed verification data in Tests/Integration/CapacityPlanningFlowTest.py"
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 for User Story 1.
3. Validate executive dashboard independently using `Scripts/RunTests.sh`, `Scripts/ValidateStack.sh`, and the quickstart critical scenario.
4. Stop and review before expanding into technical and planning dashboards.

### Incremental Delivery

1. Deliver US1 for executive decision making.
2. Deliver US2 for technical performance diagnosis.
3. Deliver US3 for service-oriented capacity planning.
4. Run Phase 6 validation after each increment and again at the end.

### Final Validation

Run:

```bash
Scripts/RunTests.sh
Scripts/ValidateStack.sh
STACK_DRY_RUN=1 Scripts/StartStack.sh
```

Then execute the real-stack validation described in `specs/004-grafana-dashboard-optimization/quickstart.md`.
