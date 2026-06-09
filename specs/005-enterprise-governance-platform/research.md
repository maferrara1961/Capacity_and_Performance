# Investigacion: Plataforma Enterprise de Gobierno

## Decision: Mantener el Toolchain Aprobado Existente

Capacity_and_Performance seguira usando Zabbix, VictoriaMetrics, PostgreSQL, Grafana, Podman,
scripts shell y Python stdlib solamente.

**Razon**: La constitucion prohibe nuevas librerias externas y el proyecto ya tiene stack funcional,
scripts de validacion, loader de datos sinteticos y modelo de provisioning de dashboards.

**Alternativas consideradas**:

- Agregar un nuevo motor analitico: rechazado porque introduce riesgo de dependencias y licencias.
- Agregar una nueva plataforma de workflow/orquestacion: rechazado porque los scripts batch
  actuales y CapacityEngine son suficientes para las evaluaciones planificadas.

## Decision: Modelar Dominios Tecnologicos como Datos

Dominios tecnologicos, tipos de componente, servicios de negocio, estados de ciclo de vida, estados
de cumplimiento y estados de evidencia se modelaran como atributos de datos y no como clases
hardcodeadas por dominio.

**Razon**: La plataforma debe soportar infraestructura, OS, bases de datos, middleware,
contenedores, mensajeria, monitoreo, aplicaciones enterprise y dominios futuros sin redisenar.

**Alternativas consideradas**:

- Caminos de codigo separados por dominio tecnologico: rechazado por duplicacion y baja
  extensibilidad.
- Texto libre solamente: rechazado porque scoring, filtros y auditabilidad requieren valores
  controlados y validacion.

## Decision: Tratar Evidencia Faltante como Estado de Primera Clase

El estado de evidencia incluira Disponible, Faltante, Desconocida, Incompleta y NoVerificada. La
evidencia faltante o debil reduce la confianza de monitoreo y no debe interpretarse como saludable.

**Razon**: La constitucion y la especificacion prohiben inferir salud desde datos faltantes.

**Alternativas consideradas**:

- Usar solo valores nulos: rechazado porque null no explica si la evidencia falta, es desconocida,
  incompleta o no verificada.
- Excluir registros incompletos: rechazado porque ocultar brechas genera falsa confianza.

## Decision: Scoring en Escala Comun 0-100

Capacity, Performance, Availability, Lifecycle, Compliance, Monitoring Confidence y Technology
Health usaran escala normalizada 0-100. La clasificacion de Technology Health es: Excellent
90-100, Healthy 75-89, Attention Required 60-74, At Risk 40-59, Critical 0-39.

**Razon**: Una escala comun permite comparacion ejecutiva y reporting reproducible.

**Alternativas consideradas**:

- Rangos de score especificos por dominio: rechazado porque complican la interpretacion ejecutiva.
- Solo estados sin puntaje: rechazado porque las partes interesadas necesitan tendencias y priorizacion.

## Decision: El Registro de Riesgos es el Objeto Compartido de Decision

Cada riesgo identificara categoria, severidad, impacto, tecnologias afectadas, servicios afectados,
estado de evidencia, referencias de evidencia y accion recomendada.

**Razon**: Esto da a ejecutivos, gobierno y operaciones un lenguaje compartido para soporte de
decisiones.

**Alternativas consideradas**:

- Riesgo solo renderizado en dashboard: rechazado porque las decisiones de riesgo requieren
  auditabilidad y reutilizacion.
- Alertas especificas por herramienta: rechazado porque las alertas crudas no incluyen contexto de
  ciclo de vida, cumplimiento y servicio de negocio.

## Decision: La Evidencia Historica es Requerida para Forecasts

Los forecasts de 30, 90, 180 y 365 dias requieren evidencia historica suficiente. Si la evidencia
es insuficiente, la salida de forecast debe mostrar un estado de evidencia insuficiente en vez de
fabricar una proyeccion.

**Razon**: Los principios de tendencia priorizan comportamiento historico sobre snapshots y exigen
trazabilidad.

**Alternativas consideradas**:

- Siempre forecast desde el ultimo punto: rechazado porque crea conclusiones no soportadas.
- Ocultar forecasts insuficientes: rechazado porque las partes interesadas deben ver brechas de
  evidencia.

## Decision: Contratos para CLI, Dataset y Dashboards

Este feature expone comportamiento operativo mediante scripts, datasets generados y dashboards
Grafana, por lo que los contratos se documentan como expectativas de comandos, datos y dashboards.

**Razon**: El proyecto no define una API web publica. Las superficies externas relevantes son
comandos, artefactos de datos y dashboards.

**Alternativas consideradas**:

- Contratos OpenAPI: rechazado porque no se define API HTTP para este feature.
- Sin contratos: rechazado porque la planificacion Spec Kit requiere expectativas testeables de
  interfaz.
