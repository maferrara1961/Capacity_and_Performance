<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Template Principle 1 -> I. Test-Driven Delivery
- Template Principle 2 -> II. SOLID and Clean Architecture
- Template Principle 3 -> III. Simplicity, DRY, and YAGNI
- Template Principle 4 -> IV. PascalCase and Dependency Discipline
- Template Principle 5 -> V. Validated Inputs and Protected Routes
Added sections:
- Engineering Constraints
- Delivery Workflow
Removed sections:
- None
Templates requiring updates:
- Updated: .specify/templates/plan-template.md
- Updated: .specify/templates/spec-template.md
- Updated: .specify/templates/tasks-template.md
- Not present: .specify/templates/commands/*.md
Follow-up TODOs:
- None
-->

# My Project Constitution

## Core Principles

### I. Test-Driven Delivery
All production behavior MUST be specified by tests before implementation. The required cycle is:
write the failing test, confirm it fails for the expected reason, implement the smallest change
that passes, then refactor while keeping the test suite green. Unit tests MUST cover business
rules, validation, and edge cases. Integration or end-to-end tests MUST cover user-visible flows,
route protection, and persistence boundaries when present.

Rationale: TDD makes requirements executable, protects refactoring, and prevents implementation
from drifting away from user scenarios.

### II. SOLID and Clean Architecture
Code MUST follow SOLID principles and Clean Architecture boundaries. Domain rules MUST remain
independent from UI, framework, transport, persistence, and infrastructure details. Dependencies
MUST point inward toward domain policy; adapters MAY depend on application interfaces, but domain
code MUST NOT depend on adapters. Each module, class, and function MUST have one clear reason to
change. Cross-boundary communication MUST use explicit interfaces or data contracts.

Rationale: Clear boundaries keep features maintainable, testable, and replaceable without broad
rewrites.

### III. Simplicity, DRY, and YAGNI
The codebase MUST avoid duplicated domain logic and repeated validation rules. Shared behavior MUST
be extracted only when there are at least two concrete uses or a clear architectural boundary that
requires it. Implementations MUST choose the simplest design that satisfies current requirements.
Speculative abstractions, unused configuration, and future-facing extension points MUST NOT be
added.

Rationale: DRY prevents inconsistent behavior, while YAGNI keeps the system small enough to reason
about safely.

### IV. PascalCase and Dependency Discipline
Project-defined code symbols and artifacts MUST use PascalCase where the language and runtime allow
it. Any unavoidable exception required by a framework, protocol, file system convention, or external
contract MUST be documented at the point of use. New external libraries, packages, SDKs, or hosted
services MUST NOT be introduced. Required capability MUST be implemented with the standard runtime,
the existing codebase, or already approved platform APIs.

Rationale: A single naming convention improves consistency, and dependency discipline reduces
supply-chain risk, version drift, and hidden complexity.

### V. Validated Inputs and Protected Routes
Every user-controlled input MUST be validated before it reaches domain logic or persistence.
Validation MUST reject malformed, missing, unauthorized, or out-of-range data with deterministic
errors. Protected routes, screens, commands, and API endpoints MUST require authentication before
executing protected behavior. Authorization checks MUST be explicit wherever user identity affects
data access or allowed actions.

Rationale: Trust boundaries are part of the architecture. Validation and authentication failures
must be predictable, testable, and closed by default.

## Engineering Constraints

Feature plans MUST define the selected Clean Architecture layers and the dependency direction
between them. Each feature MUST identify its user input boundaries, validation rules, protected
routes, and authentication assumptions before implementation starts. Any request to add an external
library or hosted service is a constitution violation unless the constitution is amended first.

Tests are mandatory deliverables, not optional supporting work. A feature is incomplete until its
tests cover the primary user stories, validation failures, authentication requirements, and the
Clean Architecture boundaries affected by the change.

## Delivery Workflow

Specifications MUST include independently testable user stories and acceptance scenarios. Plans MUST
include a Constitution Check covering TDD, SOLID, Clean Architecture, DRY, YAGNI, PascalCase, no new
external libraries, input validation, and authenticated protected routes. Task lists MUST schedule
failing tests before implementation tasks for each user story.

Code review MUST reject changes that bypass validation, skip authentication for protected routes,
introduce new external dependencies, duplicate domain logic without justification, or couple domain
logic to infrastructure concerns.

## Governance

This constitution supersedes conflicting project practices, generated plans, templates, and informal
guidance. Amendments MUST document the reason for change, the affected principles or sections, and
the migration impact on existing specs, plans, tasks, and implementation work. Compliance MUST be
reviewed during planning, task generation, implementation, and code review.

Versioning follows semantic versioning:
MAJOR for incompatible principle removals or redefinitions, MINOR for new principles or materially
expanded governance, and PATCH for wording clarifications that do not change obligations.

**Version**: 1.0.0 | **Ratified**: 2026-06-08 | **Last Amended**: 2026-06-08
