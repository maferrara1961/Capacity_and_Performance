# Plataforma Enterprise de Gobierno

## Proposito

La plataforma enterprise de gobierno extiende Capacity_and_Performance para consolidar inventario,
evidencia, scoring, riesgos, recomendaciones, tendencias y dashboards sobre dominios tecnologicos
empresariales.

## Dominios Cubiertos

- Infraestructura
- Sistemas operativos
- Bases de datos
- Middleware
- Plataformas de contenedores
- Plataformas de mensajeria
- Plataformas de monitoreo
- Aplicaciones enterprise
- Servicios de negocio

## Evidencia

Toda evaluacion debe declarar estado de evidencia:

- Available
- Missing
- Unknown
- Incomplete
- Unverified

La evidencia faltante no representa estado saludable. Los dashboards y registros deben mostrar la
brecha de evidencia en forma explicita.

## Scoring

Los scores enterprise usan rango 0-100:

- Capacity
- Performance
- Availability
- Lifecycle
- Compliance
- MonitoringConfidence
- TechnologyHealth

Clasificacion TechnologyHealth:

- 90-100: Excellent
- 75-89: Healthy
- 60-74: AttentionRequired
- 40-59: AtRisk
- 0-39: Critical

## Riesgos y Recomendaciones

Cada riesgo enterprise debe incluir categoria, severidad, impacto, tecnologias afectadas, servicios
afectados, evidencia y accion recomendada.

Las recomendaciones son soporte a decisiones humanas. No ejecutan remediacion automatica.

## Comandos Operativos

```bash
Scripts/GenerateEnterpriseVerificationData.sh --profile mixed --volume small --days 90 --load-id EnterpriseDemo001
Scripts/RunEnterpriseAssessment.sh --scope enterprise --load-id EnterpriseDemo001
Scripts/ValidateEnterpriseGovernance.sh --load-id EnterpriseDemo001
python3 -m CapacityEngine.Scheduler.SyntheticDataCommand sync-enterprise-inventory
```

## Dashboards

- Enterprise Executive Dashboard
- Enterprise Governance Dashboard
- Enterprise Operational Dashboard

Los dashboards deben distinguir "sin evidencia" de "sin riesgo".

## Datos y Correlacion

La identidad visible es el host `SRV-#####`. Ese nombre debe coincidir entre Zabbix, PostgreSQL,
VictoriaMetrics y Grafana.

VictoriaMetrics publica labels enterprise:

- `host_name`
- `technology_domain`
- `business_service`
- `business_service_id`

PostgreSQL conserva los datasets enterprise en tablas `Enterprise*`. Zabbix sigue siendo la fuente
operativa de inventario; cuando se modifique un host, ejecutar sincronizacion para reflejarlo en el
catalogo relacional.
