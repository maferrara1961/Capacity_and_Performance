# Contrato de Dataset: Plataforma Enterprise de Gobierno

## Proposito

Los datasets de gobierno enterprise deben ser consistentes entre PostgreSQL, VictoriaMetrics,
Zabbix y Grafana para que las partes interesadas vean las mismas tecnologias, servicios, evidencias,
riesgos, scores y recomendaciones.

## Grupos de Dataset Requeridos

### Inventario

- TechnologyDomain.
- TechnologyComponent.
- BusinessService.
- ServiceComponentMap.

### Evidencia

- TelemetryEvidence.
- LifecycleEvidence.
- ComplianceEvidence.
- AvailabilityEvidence.
- MonitoringCoverageEvidence.
- EvidenceState.

### Evaluacion

- AssessmentRun.
- ScoreAssessment.
- RiskAssessment.
- ForecastResult.
- RiskRegistryEntry.
- Recommendation.

## Consistencia de Identidad

- El nombre visible del componente debe ser estable entre Zabbix, PostgreSQL, labels de
  VictoriaMetrics y paneles Grafana.
- Pueden existir identificadores internos para joins y limpieza, pero los dashboards ejecutivos
  deben mostrar nombres legibles por negocio.
- Las referencias a servicios de negocio deben ser compartidas por scores, riesgos y
  recomendaciones.

## Reglas de Estado de Evidencia

- Evidencia disponible puede soportar estado saludable solo cuando los criterios de riesgo pasan.
- Evidencia faltante no puede soportar estado saludable, compliant o supported.
- Evidencia desconocida debe permanecer visible en dashboards y registros.
- Evidencia incompleta debe reducir Monitoring Confidence Score.
- Evidencia no verificada debe requerir revision antes de soportar conclusiones finales.

## Reglas de Score

- Todos los scores son enteros o decimales en rango 0-100.
- La clasificacion de Technology Health Score usa los umbrales requeridos:
  - 90-100: Excellent.
  - 75-89: Healthy.
  - 60-74: Attention Required.
  - 40-59: At Risk.
  - 0-39: Critical.

## Reglas de Forecast

- Los forecasts deben incluir 30 y 90 dias cuando exista evidencia suficiente.
- Los forecasts deben incluir 180 y 365 dias cuando exista historia suficiente.
- Historia insuficiente debe producir una limitacion explicita de evidencia.

## Reglas de Borrado

- Los datasets generados de verificacion deben poder borrarse por load id.
- El modo delete-all debe requerir confirmacion explicita.
- El borrado no debe eliminar inventario operativo no generado ni evidencia administrada
  manualmente.
