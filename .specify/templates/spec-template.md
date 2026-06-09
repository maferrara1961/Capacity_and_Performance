# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`

**Created**: [DATE]

**Status**: Draft

**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]
- **FR-006**: System MUST validate every user-controlled input before domain logic or persistence
- **FR-007**: System MUST require authentication for every protected route, screen, command, or API endpoint
- **FR-008**: System MUST enforce authorization wherever user identity changes data access or allowed actions
- **FR-009**: System MUST satisfy the feature without adding external libraries, SDKs, packages, or hosted services
- **FR-010**: Project-defined code symbols and artifacts MUST use PascalCase unless a documented platform convention requires otherwise
- **FR-011**: System MUST explicitly represent missing, unknown, incomplete, and unverified evidence states
- **FR-012**: System MUST NOT present missing evidence as healthy status
- **FR-013**: System MUST calculate risk or score outputs using objective and reproducible criteria
- **FR-014**: System MUST identify affected technologies and services for every risk assessment or recommendation

*Example of marking unclear requirements:*

- **FR-015**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-016**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

## Constitution Alignment *(mandatory)*

- **Testability**: [Describe how acceptance scenarios become failing tests before implementation]
- **Clean Architecture**: [Identify domain/application/adapter/infrastructure boundaries affected by this feature]
- **Validation**: [List user-controlled inputs and required validation outcomes]
- **Protected Access**: [List protected routes/screens/commands/API endpoints and authentication expectations]
- **Dependency Constraint**: [Confirm no new external libraries/services are required, or mark constitution conflict]
- **Naming**: [Confirm PascalCase applies to project-defined symbols/artifacts or document required exceptions]
- **Platform Domains**: [Identify affected domains: Capacity, Performance, Availability, Lifecycle, Compliance, Monitoring Governance]
- **Evidence Model**: [List measurable evidence sources and missing/unknown/incomplete/unverified behavior]
- **Risk and Scoring**: [Define objective criteria, affected technologies/services, and 0-100 score behavior if applicable]
- **Trend Priority**: [Describe historical trend or forecast behavior, or state why snapshots are sufficient]
- **Decision Support**: [Explain recommendation outputs and how authorized personnel retain final decision authority]

## Assumptions

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right assumptions based on reasonable defaults
  chosen when the feature description did not specify certain details.
-->

- [Assumption about target users, e.g., "Users have stable internet connectivity"]
- [Assumption about scope boundaries, e.g., "Mobile support is out of scope for v1"]
- [Assumption about data/environment, e.g., "Existing authentication system will be reused"]
- [Dependency on existing system/service, e.g., "Requires access to the existing user profile API"]
