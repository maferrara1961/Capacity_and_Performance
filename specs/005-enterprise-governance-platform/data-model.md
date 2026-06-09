# Modelo de Datos: Plataforma Enterprise de Gobierno

## TechnologyDomain

Representa un dominio tecnologico enterprise soportado.

**Campos**:

- `DomainId`: identificador estable.
- `Name`: Infrastructure, OperatingSystem, Database, Middleware, ContainerPlatform,
  MessagingPlatform, MonitoringPlatform, EnterpriseApplication o BusinessService.
- `Description`: descripcion legible por negocio.
- `Status`: Active, Deprecated o Disabled.

**Reglas de Validacion**:

- `Name` es requerido y unico.
- Dominios Disabled no pueden recibir nuevos registros de inventario.

## TechnologyComponent

Representa un elemento tecnologico monitoreado o gobernado.

**Campos**:

- `ComponentId`: identificador estable.
- `ComponentName`: nombre visible.
- `TechnologyType`: servidor, maquina virtual, base de datos, middleware, aplicacion, servicio u
  otro valor controlado.
- `DomainId`: TechnologyDomain asociado.
- `Version`: version tecnologica cuando exista.
- `Vendor`: vendor o proveedor.
- `Environment`: Production, NonProduction, Development, Test o Unknown.
- `BusinessServiceId`: servicio de negocio asociado opcional.
- `Owner`: owner o equipo responsable.
- `SupportStatus`: Supported, Backlevel, EndOfSupport, EndOfLife o Unknown.
- `LifecycleStatus`: Current, AttentionRequired, AtRisk, Critical o Unknown.
- `EvidenceState`: Available, Missing, Unknown, Incomplete o Unverified.

**Relaciones**:

- Pertenece a un TechnologyDomain.
- Puede soportar uno o mas BusinessServices mediante ServiceComponentMap.
- Tiene muchos EvidenceRecords, RiskAssessments y ScoreAssessments.

**Reglas de Validacion**:

- `ComponentName`, `TechnologyType`, `DomainId` y `EvidenceState` son requeridos.
- Evidencia faltante de ciclo de vida debe producir `SupportStatus = Unknown` o
  `LifecycleStatus = Unknown`.

## BusinessService

Representa un servicio o agrupacion de aplicacion orientada al negocio.

**Campos**:

- `BusinessServiceId`: identificador estable.
- `ServiceName`: nombre visible del servicio.
- `ServiceOwner`: owner o equipo responsable.
- `Criticality`: Low, Medium, High o Critical.
- `Status`: Active, Degraded, Critical, Retired o Unknown.

**Relaciones**:

- Tiene muchos TechnologyComponents mediante ServiceComponentMap.
- Tiene muchos RiskRegistryEntries mediante mapeos de servicios afectados.

## ServiceComponentMap

Mapea componentes tecnologicos a servicios de negocio.

**Campos**:

- `MapId`: identificador estable.
- `BusinessServiceId`: referencia al servicio.
- `ComponentId`: referencia al componente.
- `Role`: Application, Database, Middleware, Storage, Network, Monitoring u Other.
- `ImpactWeight`: contribucion numerica al riesgo del servicio.

**Reglas de Validacion**:

- `ImpactWeight` debe estar entre 0 y 100.
- Un componente compartido por multiples servicios debe permanecer visible en cada contexto de
  servicio afectado.

## EvidenceRecord

Representa evidencia usada por evaluaciones.

**Campos**:

- `EvidenceId`: identificador estable.
- `SourceSystem`: Zabbix, VictoriaMetrics, PostgreSQL, ManualRecord, SyntheticDataset u Other.
- `EvidenceType`: Telemetry, Inventory, Availability, Event, Lifecycle, Compliance, Trend o
  Forecast.
- `ComponentId`: referencia opcional al componente.
- `BusinessServiceId`: referencia opcional al servicio.
- `ObservedAt`: timestamp de la evidencia.
- `FreshnessStatus`: Fresh, Stale, Expired o Unknown.
- `EvidenceState`: Available, Missing, Unknown, Incomplete o Unverified.
- `EvidenceReference`: consulta fuente, id de registro, label de metrica, referencia de dashboard
  o path de archivo.

**Reglas de Validacion**:

- Toda evaluacion debe referenciar al menos un EvidenceRecord o un estado explicito de evidencia
  faltante.
- Evidencia stale o incompleta debe reducir MonitoringConfidenceScore.

## AssessmentRun

Representa una ejecucion de calculos de evaluacion enterprise.

**Campos**:

- `AssessmentRunId`: identificador estable.
- `StartedAt`: timestamp de inicio.
- `CompletedAt`: timestamp opcional de fin.
- `Status`: Running, Succeeded, Failed o Partial.
- `Scope`: alcance domain, component, service o enterprise.
- `EvidenceWindowStart`: inicio de la ventana de evidencia.
- `EvidenceWindowEnd`: fin de la ventana de evidencia.

## ScoreAssessment

Representa un score 0-100 para un area de evaluacion.

**Campos**:

- `ScoreAssessmentId`: identificador estable.
- `AssessmentRunId`: referencia al run.
- `ScoreType`: Capacity, Performance, Availability, Lifecycle, Compliance, MonitoringConfidence o
  TechnologyHealth.
- `ScopeType`: Enterprise, Domain, BusinessService o TechnologyComponent.
- `ScopeId`: identificador de alcance referenciado.
- `ScoreValue`: 0-100.
- `Classification`: Excellent, Healthy, AttentionRequired, AtRisk o Critical.
- `EvidenceState`: Available, Missing, Unknown, Incomplete o Unverified.
- `CalculatedAt`: timestamp.

**Reglas de Validacion**:

- `ScoreValue` debe estar entre 0 y 100.
- La clasificacion TechnologyHealth debe seguir umbrales 90/75/60/40.
- Evidencia faltante no puede producir clasificacion Excellent o Healthy.

## RiskAssessment

Representa un riesgo especifico de dominio calculado desde evidencia.

**Campos**:

- `RiskAssessmentId`: identificador estable.
- `AssessmentRunId`: referencia al run.
- `RiskCategory`: Capacity, Performance, Availability, Lifecycle, Compliance o Monitoring.
- `Severity`: Low, Medium, High o Critical.
- `Impact`: impacto legible por negocio.
- `ScopeType`: Enterprise, Domain, BusinessService o TechnologyComponent.
- `ScopeId`: identificador de alcance referenciado.
- `EvidenceState`: Available, Missing, Unknown, Incomplete o Unverified.
- `Reason`: explicacion.
- `CalculatedAt`: timestamp.

**Reglas de Validacion**:

- Cada riesgo debe identificar tecnologias y servicios afectados mediante mapeos de
  RiskRegistryEntry.
- Los riesgos deben ser reproducibles desde la evidencia referenciada.

## RiskRegistryEntry

Representa el objeto compartido de riesgo para gobierno y decisiones ejecutivas.

**Campos**:

- `RiskId`: identificador estable del riesgo.
- `RiskAssessmentId`: referencia a la evaluacion.
- `RiskCategory`: Capacity, Performance, Availability, Lifecycle, Compliance o Monitoring.
- `Severity`: Low, Medium, High o Critical.
- `Impact`: impacto legible por negocio.
- `AffectedTechnologyIds`: una o mas referencias a TechnologyComponent.
- `AffectedServiceIds`: cero o mas referencias a BusinessService.
- `RecommendedAction`: propuesta de accion.
- `Status`: Open, Accepted, Mitigating, Closed o Deferred.
- `Owner`: owner o equipo responsable.
- `EvidenceState`: Available, Missing, Unknown, Incomplete o Unverified.

**Reglas de Validacion**:

- Todo riesgo abierto debe incluir severidad, impacto, tecnologias afectadas y accion recomendada.
- Si no existe mapeo de servicio, el riesgo debe mostrar la brecha de mapeo en lugar de ocultar el
  componente.

## Recommendation

Representa una recomendacion de soporte a decision.

**Campos**:

- `RecommendationId`: identificador estable.
- `RiskId`: referencia al riesgo.
- `Priority`: Low, Medium, High o Critical.
- `Action`: accion recomendada.
- `Rationale`: razon respaldada por evidencia.
- `DecisionOwner`: owner o equipo autorizado para decidir.
- `Status`: Open, Accepted, Rejected, Completed o Deferred.

**Reglas de Validacion**:

- Las recomendaciones no deben ejecutar remediacion automaticamente.
- Las recomendaciones deben referenciar evidencia y tecnologias/servicios afectados mediante el
  riesgo.

## ForecastResult

Representa un forecast derivado de evidencia historica.

**Campos**:

- `ForecastId`: identificador estable.
- `AssessmentRunId`: referencia al run.
- `ComponentId`: referencia al componente.
- `MetricName`: CPU, Memory, Storage, Filesystem u otro valor controlado.
- `Forecast30Days`: valor proyectado opcional.
- `Forecast90Days`: valor proyectado opcional.
- `Forecast180Days`: valor proyectado opcional.
- `Forecast365Days`: valor proyectado opcional.
- `DaysToExhaustion`: dias opcionales hasta saturacion o agotamiento.
- `EvidenceState`: Available, Missing, Unknown, Incomplete o Unverified.
- `Confidence`: Low, Medium o High.

**Reglas de Validacion**:

- Horizontes de forecast sin historia suficiente deben quedar vacios e informar evidencia
  insuficiente.
- Los forecasts deben identificar ventana de evidencia fuente y componente.

## Transiciones de Estado

### RiskRegistryEntry.Status

```text
Open -> Accepted -> Mitigating -> Closed
Open -> Deferred
Open -> Closed
Open -> Rejected
Deferred -> Accepted
Mitigating -> Deferred
```

### EvidenceState

```text
Unknown -> Available
Unknown -> Missing
Available -> Incomplete
Available -> Unverified
Incomplete -> Available
Unverified -> Available
Available -> Missing
```
