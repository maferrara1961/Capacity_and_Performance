# Tasks: Capacity Observability Stack

**Input**: Design documents from `/specs/001-capacity-observability-stack/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are mandatory by constitution. Each user story includes failing test tasks before
implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing
of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files and has no dependency on incomplete tasks
- **[Story]**: User story label for story phases only
- Every task includes concrete file paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the repository structure, no-license-cost stack skeleton, and validation entry points.

- [X] T001 Create project directories in ContainerImages/Zabbix, ContainerImages/VictoriaMetrics, ContainerImages/Grafana, ContainerImages/PostgreSQL, ContainerImages/CapacityEngine, Config/Grafana/Dashboards, Config/Grafana/Datasources, Config/Zabbix, Config/VictoriaMetrics, Config/PostgreSQL, CapacityEngine/Domain, CapacityEngine/Application, CapacityEngine/Adapters, CapacityEngine/Scheduler, CapacityEngine/Tests, Scripts, Sql/Schema, Sql/Seed, Sql/Validation, Tests/Contract, Tests/Integration, Tests/Unit
- [X] T002 Create Python package marker files in CapacityEngine/__init__.py, CapacityEngine/Domain/__init__.py, CapacityEngine/Application/__init__.py, CapacityEngine/Adapters/__init__.py, CapacityEngine/Scheduler/__init__.py, CapacityEngine/Tests/__init__.py
- [X] T003 Create stack manifest documenting approved runtime components in Config/StackManifest.yml
- [X] T004 Create Podman compose-style stack definition in Config/PodmanStack.yml
- [X] T005 [P] Create Zabbix image definition in ContainerImages/Zabbix/Containerfile
- [X] T006 [P] Create VictoriaMetrics image definition in ContainerImages/VictoriaMetrics/Containerfile
- [X] T007 [P] Create Grafana image definition in ContainerImages/Grafana/Containerfile
- [X] T008 [P] Create PostgreSQL image definition in ContainerImages/PostgreSQL/Containerfile
- [X] T009 [P] Create CapacityEngine image definition in ContainerImages/CapacityEngine/Containerfile
- [X] T010 Create stack startup script in Scripts/StartStack.sh
- [X] T011 Create stack stop script in Scripts/StopStack.sh
- [X] T012 Create stack validation script in Scripts/ValidateStack.sh
- [X] T013 Create daily capacity runner script in Scripts/RunCapacityDaily.sh
- [X] T014 Create Python unittest runner script in Scripts/RunTests.sh

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the shared domain, validation, persistence, and security foundation required by all stories.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T015 [P] Create domain constants and enumerations in CapacityEngine/Domain/Constants.py
- [X] T016 [P] Create domain exception types in CapacityEngine/Domain/Exceptions.py
- [X] T017 [P] Create validation utilities in CapacityEngine/Domain/Validators.py
- [X] T018 Create core entity models for Service, Application, MonitoredResource, ServiceResourceMap, MetricSample, AlertThreshold, Baseline, CapacityKpi, ForecastResult, RiskAssessment, Recommendation, and CapacityRun in CapacityEngine/Domain/Entities.py
- [X] T019 Create domain repository interfaces in CapacityEngine/Application/Ports.py
- [X] T020 Create authentication and authorization boundary interfaces in CapacityEngine/Application/Security.py
- [X] T021 Create capacity calculation service skeleton in CapacityEngine/Application/CapacityCalculator.py
- [X] T022 Create risk scoring service skeleton in CapacityEngine/Application/RiskScorer.py
- [X] T023 Create recommendation service skeleton in CapacityEngine/Application/RecommendationService.py
- [X] T024 Create service catalog application service skeleton in CapacityEngine/Application/ServiceCatalogService.py
- [X] T025 Create PostgreSQL schema for catalog entities in Sql/Schema/001_Catalog.sql
- [X] T026 Create PostgreSQL schema for capacity outputs and run history in Sql/Schema/002_CapacityOutputs.sql
- [X] T027 Create SQL validation checks for required catalog fields in Sql/Validation/ValidateCatalog.sql
- [X] T028 Create SQL validation checks for capacity output consistency in Sql/Validation/ValidateCapacityOutputs.sql
- [X] T029 Create sample services, applications, resources, thresholds, and baselines in Sql/Seed/SampleCatalog.sql
- [X] T030 Create PostgreSQL command adapter using approved platform commands in CapacityEngine/Adapters/PostgreSqlCommandAdapter.py
- [X] T031 Create VictoriaMetrics query adapter skeleton in CapacityEngine/Adapters/VictoriaMetricsAdapter.py
- [X] T032 Create scheduler entry point for daily execution in CapacityEngine/Scheduler/DailyCapacityRun.py
- [X] T033 Create Grafana datasource provisioning file in Config/Grafana/Datasources/Datasources.yml
- [X] T034 Create dashboard provisioning file in Config/Grafana/Dashboards/Provisioning.yml
- [X] T035 Create foundational validation tests in Tests/Unit/FoundationValidationTest.py

**Checkpoint**: Foundation ready; user story implementation can proceed.

---

## Phase 3: User Story 1 - Visualizar riesgo ejecutivo de capacidad (Priority: P1)

**Goal**: Executive users can see global capacity state, saturation risks, 30/60/90 day forecasts,
used versus available capacity, and recommendations.

**Independent Test**: Load sample services and metrics, run the capacity calculation, and verify the
executive dashboard model shows OK/Warning/Critical state, risky services, forecasts, and actions.

### Tests for User Story 1 (MANDATORY - write before implementation)

- [X] T036 [P] [US1] Create failing unit tests for average, peak, p95, headroom, monthly growth, and days-to-saturation calculations in Tests/Unit/CapacityCalculatorTest.py
- [X] T037 [P] [US1] Create failing unit tests for OK, Warning, and Critical risk classification in Tests/Unit/RiskScorerTest.py
- [X] T038 [P] [US1] Create failing contract tests for CapacityEngineContract outputs in Tests/Contract/CapacityEngineContractTest.py
- [X] T039 [P] [US1] Create failing dashboard contract tests for Executive Capacity Dashboard requirements in Tests/Contract/ExecutiveDashboardContractTest.py
- [X] T040 [US1] Create failing integration test for daily capacity run feeding executive outputs in Tests/Integration/ExecutiveCapacityFlowTest.py

### Implementation for User Story 1

- [X] T041 [US1] Implement KPI formulas in CapacityEngine/Application/CapacityCalculator.py
- [X] T042 [US1] Implement forecast 30/60/90 day and days-to-saturation logic in CapacityEngine/Application/CapacityCalculator.py
- [X] T043 [US1] Implement risk scoring for CPU, RAM, storage, IOPS, and network in CapacityEngine/Application/RiskScorer.py
- [X] T044 [US1] Implement recommendation generation for Warning and Critical risk in CapacityEngine/Application/RecommendationService.py
- [X] T045 [US1] Implement daily capacity run orchestration in CapacityEngine/Scheduler/DailyCapacityRun.py
- [X] T046 [US1] Implement persistence mapping for CapacityKpi, ForecastResult, RiskAssessment, Recommendation, and CapacityRun in CapacityEngine/Adapters/PostgreSqlCommandAdapter.py
- [X] T047 [US1] Create Executive Capacity Dashboard JSON in Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json
- [X] T048 [US1] Add executive dashboard validation rules to Scripts/ValidateStack.sh
- [X] T049 [US1] Add sample warning and critical capacity data in Sql/Seed/SampleCatalog.sql
- [X] T050 [US1] Verify User Story 1 tests pass via Scripts/RunTests.sh

**Checkpoint**: User Story 1 is fully functional and independently testable.

---

## Phase 4: User Story 2 - Analizar performance tecnica por plataforma (Priority: P2)

**Goal**: Technical users can inspect CPU, memory, disk, network, IOPS, latency, throughput,
errors, saturation, average, peak, p95, and threshold breaches by platform and resource.

**Independent Test**: Select a platform with known metrics and verify the technical dashboard model
shows raw metrics, derived values, and visual threshold breach state.

### Tests for User Story 2 (MANDATORY - write before implementation)

- [X] T051 [P] [US2] Create failing unit tests for metric sample validation and duplicate handling in Tests/Unit/MetricSampleValidationTest.py
- [X] T052 [P] [US2] Create failing unit tests for threshold comparison behavior in Tests/Unit/AlertThresholdTest.py
- [X] T053 [P] [US2] Create failing contract tests for Technical Performance Dashboard requirements in Tests/Contract/TechnicalDashboardContractTest.py
- [X] T054 [US2] Create failing integration test for platform metric drilldown in Tests/Integration/TechnicalPerformanceFlowTest.py

### Implementation for User Story 2

- [X] T055 [US2] Implement metric sample validation in CapacityEngine/Domain/Validators.py
- [X] T056 [US2] Implement threshold comparison logic in CapacityEngine/Application/RiskScorer.py
- [X] T057 [US2] Implement VictoriaMetrics query mapping for CPU, RAM, storage, IOPS, network, latency, throughput, errors, and saturation in CapacityEngine/Adapters/VictoriaMetricsAdapter.py
- [X] T058 [US2] Create Technical Performance Dashboard JSON in Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json
- [X] T059 [US2] Add technical dashboard validation rules to Scripts/ValidateStack.sh
- [X] T060 [US2] Add sample technical metric data in Sql/Seed/SampleCatalog.sql
- [X] T061 [US2] Verify User Story 2 tests pass via Scripts/RunTests.sh

**Checkpoint**: User Story 2 works independently after the shared foundation.

---

## Phase 5: User Story 3 - Planificar capacidad por servicio y aplicacion (Priority: P3)

**Goal**: Capacity planners can review trends, monthly growth, exhaustion dates, oversized
resources, undersized resources, headroom, baseline comparison, forecasts, and top consumers.

**Independent Test**: Run the daily capacity calculation against historical sample data and verify
growth, forecast windows, exhaustion estimates, top consumers, and sizing classifications.

### Tests for User Story 3 (MANDATORY - write before implementation)

- [X] T062 [P] [US3] Create failing unit tests for baseline comparison in Tests/Unit/BaselineComparisonTest.py
- [X] T063 [P] [US3] Create failing unit tests for top consumer ranking and oversized or undersized classification in Tests/Unit/CapacityPlanningTest.py
- [X] T064 [P] [US3] Create failing contract tests for Capacity Planning Dashboard requirements in Tests/Contract/CapacityPlanningDashboardContractTest.py
- [X] T065 [US3] Create failing integration test for daily planning outputs in Tests/Integration/CapacityPlanningFlowTest.py

### Implementation for User Story 3

- [X] T066 [US3] Implement baseline delta calculations in CapacityEngine/Application/CapacityCalculator.py
- [X] T067 [US3] Implement top consumer ranking in CapacityEngine/Application/CapacityCalculator.py
- [X] T068 [US3] Implement oversized and undersized resource classification in CapacityEngine/Application/RiskScorer.py
- [X] T069 [US3] Extend PostgreSQL capacity output queries for planning views in CapacityEngine/Adapters/PostgreSqlCommandAdapter.py
- [X] T070 [US3] Create Capacity Planning Dashboard JSON in Config/Grafana/Dashboards/CapacityPlanningDashboard.json
- [X] T071 [US3] Add capacity planning validation rules to Scripts/ValidateStack.sh
- [X] T072 [US3] Add historical growth and low-utilization sample data in Sql/Seed/SampleCatalog.sql
- [X] T073 [US3] Verify User Story 3 tests pass via Scripts/RunTests.sh

**Checkpoint**: User Story 3 works independently after the shared foundation.

---

## Phase 6: User Story 4 - Navegar catalogo de servicios y dependencias (Priority: P4)

**Goal**: Service owners can navigate services, applications, servers, databases, storage, network,
dependencies, SLA/SLO state, end-to-end performance, and dependency-driven risk.

**Independent Test**: Register a service with mapped components and verify the application dashboard
shows all infrastructure and propagates degraded dependency risk.

### Tests for User Story 4 (MANDATORY - write before implementation)

- [X] T074 [P] [US4] Create failing unit tests for service catalog completeness and mapping validation in Tests/Unit/ServiceCatalogValidationTest.py
- [X] T075 [P] [US4] Create failing contract tests for ServiceCatalogContract behavior in Tests/Contract/ServiceCatalogContractTest.py
- [X] T076 [P] [US4] Create failing contract tests for Application Dashboard requirements in Tests/Contract/ApplicationDashboardContractTest.py
- [X] T077 [US4] Create failing integration test for dependency risk propagation in Tests/Integration/ApplicationDashboardFlowTest.py

### Implementation for User Story 4

- [X] T078 [US4] Implement service catalog validation and completeness rules in CapacityEngine/Application/ServiceCatalogService.py
- [X] T079 [US4] Implement shared-resource and dependency mapping behavior in CapacityEngine/Application/ServiceCatalogService.py
- [X] T080 [US4] Implement dependency risk propagation into application and service risk in CapacityEngine/Application/RiskScorer.py
- [X] T081 [US4] Extend catalog persistence queries for service, application, resource, and dependency mappings in CapacityEngine/Adapters/PostgreSqlCommandAdapter.py
- [X] T082 [US4] Create Application Dashboard JSON in Config/Grafana/Dashboards/ApplicationDashboard.json
- [X] T083 [US4] Add application dashboard and catalog validation rules to Scripts/ValidateStack.sh
- [X] T084 [US4] Add complete and incomplete service mapping sample data in Sql/Seed/SampleCatalog.sql
- [X] T085 [US4] Verify User Story 4 tests pass via Scripts/RunTests.sh

**Checkpoint**: User Story 4 works independently after the shared foundation.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validate the full stack, remove duplication, and ensure governance compliance.

- [X] T086 Run all unit, contract, and integration tests in Scripts/RunTests.sh
- [X] T087 Run quickstart stack validation scenarios in Scripts/ValidateStack.sh
- [X] T088 Verify Podman startup and shutdown scripts against Config/PodmanStack.yml in Scripts/StartStack.sh and Scripts/StopStack.sh
- [X] T089 Verify no external application-code libraries are introduced in Config/StackManifest.yml and ContainerImages/CapacityEngine/Containerfile
- [X] T090 Verify project-defined symbols and artifacts follow PascalCase or document platform exceptions in docs/PascalCaseExceptions.md
- [X] T091 Remove duplicated capacity formula or validation logic across CapacityEngine/Application/CapacityCalculator.py, CapacityEngine/Application/RiskScorer.py, and CapacityEngine/Domain/Validators.py
- [X] T092 Add final operational documentation in docs/CapacityObservabilityStack.md
- [X] T093 Update quickstart validation results in specs/001-capacity-observability-stack/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; starts immediately.
- **Phase 2 Foundational**: Depends on Phase 1 completion; blocks all user stories.
- **Phase 3 US1**: Depends on Phase 2; recommended MVP.
- **Phase 4 US2**: Depends on Phase 2; can run after or in parallel with US1 if staffing allows.
- **Phase 5 US3**: Depends on Phase 2 and benefits from US1 capacity outputs.
- **Phase 6 US4**: Depends on Phase 2 and benefits from US1 risk outputs.
- **Phase 7 Polish**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Required MVP; creates core KPI, forecast, risk, recommendation, and executive outputs.
- **US2 (P2)**: Uses shared metrics and threshold foundation; independently testable.
- **US3 (P3)**: Extends capacity outputs for planning; can validate independently with historical samples.
- **US4 (P4)**: Extends catalog and dependency mapping; can validate independently with mapped samples.

### Within Each User Story

- Tests MUST be written and confirmed failing before implementation.
- Domain model and validation tasks precede application services.
- Application services precede adapters and dashboard provisioning.
- Dashboard validation tasks follow dashboard JSON creation.
- Story verification task closes each story.

## Parallel Opportunities

- Setup image definitions T005-T009 can run in parallel.
- Foundational domain and SQL tasks T015-T017 and T025-T029 can run in parallel after directories exist.
- Test tasks inside each user story can run in parallel when they touch different files.
- Dashboard JSON tasks for US1-US4 can run in parallel after foundational provisioning exists.
- Polish verification tasks T089-T092 can run in parallel after all selected stories pass.

## Parallel Example: User Story 1

```bash
Task: "Create failing unit tests for average, peak, p95, headroom, monthly growth, and days-to-saturation calculations in Tests/Unit/CapacityCalculatorTest.py"
Task: "Create failing unit tests for OK, Warning, and Critical risk classification in Tests/Unit/RiskScorerTest.py"
Task: "Create failing contract tests for CapacityEngineContract outputs in Tests/Contract/CapacityEngineContractTest.py"
Task: "Create failing dashboard contract tests for Executive Capacity Dashboard requirements in Tests/Contract/ExecutiveDashboardContractTest.py"
```

## Parallel Example: User Story 2

```bash
Task: "Create failing unit tests for metric sample validation and duplicate handling in Tests/Unit/MetricSampleValidationTest.py"
Task: "Create failing unit tests for threshold comparison behavior in Tests/Unit/AlertThresholdTest.py"
Task: "Create failing contract tests for Technical Performance Dashboard requirements in Tests/Contract/TechnicalDashboardContractTest.py"
```

## Parallel Example: User Story 3

```bash
Task: "Create failing unit tests for baseline comparison in Tests/Unit/BaselineComparisonTest.py"
Task: "Create failing unit tests for top consumer ranking and oversized or undersized classification in Tests/Unit/CapacityPlanningTest.py"
Task: "Create failing contract tests for Capacity Planning Dashboard requirements in Tests/Contract/CapacityPlanningDashboardContractTest.py"
```

## Parallel Example: User Story 4

```bash
Task: "Create failing unit tests for service catalog completeness and mapping validation in Tests/Unit/ServiceCatalogValidationTest.py"
Task: "Create failing contract tests for ServiceCatalogContract behavior in Tests/Contract/ServiceCatalogContractTest.py"
Task: "Create failing contract tests for Application Dashboard requirements in Tests/Contract/ApplicationDashboardContractTest.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete Phase 3 User Story 1.
4. Stop and validate Executive Capacity Dashboard behavior independently.

### Incremental Delivery

1. Deliver US1 for executive capacity risk.
2. Add US2 for technical troubleshooting.
3. Add US3 for capacity planning.
4. Add US4 for catalog and dependency navigation.
5. Run Phase 7 polish and full validation.

### Validation Gates

- No implementation task starts before its failing tests exist.
- Each story verification task must pass before moving to the next story in sequential delivery.
- Quickstart validation must pass before the feature is considered complete.

## Summary

- Total tasks: 93
- Setup tasks: 14
- Foundational tasks: 21
- US1 tasks: 15
- US2 tasks: 11
- US3 tasks: 12
- US4 tasks: 12
- Polish tasks: 8
- MVP scope: Phase 1, Phase 2, and Phase 3 (US1)
