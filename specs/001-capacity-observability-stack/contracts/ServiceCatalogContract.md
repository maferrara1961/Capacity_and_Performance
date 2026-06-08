# Contract: Service Catalog

## Purpose

Defines how infrastructure is mapped to services and applications for capacity reporting.

## Catalog Entry Contract

Each service entry MUST include:
- Service identifier.
- Service name.
- Owner.
- Criticality.
- At least one mapped resource before the service is considered complete.

Each application entry MUST include:
- Application identifier.
- Parent service identifier.
- Application name.
- Environment.

Each resource mapping MUST include:
- Resource identifier.
- Resource type.
- Service identifier.
- Optional application identifier.
- Role.
- Impact weight.

## Supported Resource Types

- Server.
- Database.
- Storage.
- Network.
- Dependency.
- ApplicationComponent.

## Validation Contract

The catalog MUST reject:
- Missing service names.
- Duplicate service identifiers.
- Mappings to nonexistent resources.
- Impact weights outside 1 to 100.
- Unsupported resource types.
- Unsupported criticality values.

The catalog MUST allow:
- Shared resources mapped to multiple services.
- Services with incomplete mappings, marked as incomplete until resolved.
- Manual ownership and criticality values when discovery data is unavailable.

## Completeness Contract

A service is complete when:
- It has an owner.
- It has criticality.
- It has at least one mapped resource.
- Known servers, databases, storage, network resources, and dependencies are represented or
  explicitly marked as not applicable.

## Protected Access Contract

Catalog read and write actions MUST require authentication. Catalog write actions MUST require an
authorized operator or administrator role.
