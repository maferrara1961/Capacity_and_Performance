# Contrato de Dashboards: Plataforma Enterprise de Gobierno

## Dashboard Ejecutivo

El dashboard ejecutivo debe permitir que un usuario ejecutivo entienda la salud tecnologica
enterprise en sesenta segundos.

### Paneles Requeridos

- Technology Health Score.
- Capacity Score.
- Performance Score.
- Availability Score.
- Lifecycle Score.
- Compliance Score.
- Monitoring Confidence Score.
- Risk Heat Map por dominio tecnologico.
- Top 10 Riesgos con severidad, impacto, tecnologias afectadas, servicios afectados y accion.
- Capacity Forecast para CPU, memoria y storage.
- Lifecycle Overview.
- Compliance Overview.
- Service Health Overview.
- Executive Decision Summary.

### Comportamiento ante Vacio y Evidencia Faltante

- La evidencia faltante debe mostrarse como faltante, desconocida, incompleta o no verificada.
- La evidencia faltante no debe renderizarse como OK, Healthy, Compliant o Supported.
- Los dashboards deben incluir contexto suficiente para distinguir "sin riesgo" de "sin evidencia".

## Dashboard de Gobierno

El dashboard de gobierno soporta service delivery managers, platform owners y usuarios de
cumplimiento.

### Paneles Requeridos

- Inventario tecnologico por dominio.
- Mapeo servicio-componente.
- Estado de ciclo de vida por tecnologia.
- Estado de cumplimiento por tecnologia.
- Cobertura y frescura de monitoreo.
- Registro de riesgos.
- Recomendaciones abiertas por owner y severidad.

## Dashboard Operativo

El dashboard operativo soporta equipos de ingenieria y operaciones.

### Paneles Requeridos

- Tendencias de capacidad.
- Tendencias de performance.
- Historia de disponibilidad.
- Top consumidores.
- Indicadores de saturacion.
- Horizontes de forecast para 30, 90, 180 y 365 dias.
- Frescura de evidencia y fallas de recoleccion.

## Filtros

Los dashboards deben soportar, cuando existan datos:

- Run de evaluacion.
- Dominio tecnologico.
- Servicio de negocio.
- Ambiente.
- Severidad.
- Estado de evidencia.

## Validacion

Las pruebas contract deben inspeccionar artefactos de provisioning de dashboards y confirmar que
titulos, queries, datasources, filtros y texto de evidencia faltante requeridos esten presentes.
