# Research: Datos de Prueba para Monitoreo, Performance y Capacity

## Decision: Generador Python con libreria estandar

**Rationale**: La constitucion prohibe nuevas librerias externas y el proyecto ya usa Python estandar para `CapacityEngine`. Un comando Python permite generar datos deterministas con semilla opcional, validar argumentos y coordinar adaptadores sin introducir dependencias.

**Alternatives considered**:
- Bash puro: descartado por mayor complejidad para modelos, aleatoriedad controlada y validacion.
- Herramientas externas de carga: descartadas por costo de dependencia y violacion constitucional.

## Decision: Lotes identificados y marcados como datos de prueba

**Rationale**: El borrado seguro requiere distinguir datos sinteticos de datos operativos. Cada carga tendra `LoadId`, marca de prueba, perfil de escenario y conteos para auditoria.

**Alternatives considered**:
- Borrado por fecha: descartado porque podria eliminar datos no sinteticos.
- Borrado total de tablas: descartado por riesgo operacional.

## Decision: Escenarios sinteticos predefinidos

**Rationale**: Los dashboards necesitan datos variados: normal, warning, critical, overprovisioned y underprovisioned. Perfiles predefinidos permiten validar visualizaciones y umbrales de forma repetible.

**Alternatives considered**:
- Aleatoriedad sin perfil: descartada porque no garantiza cobertura de paneles.
- Datos fijos unicos: descartados porque no validan multiples cargas ni variabilidad.

## Decision: Contrato CLI con acciones load, list, validate y delete

**Rationale**: La operacion solicitada requiere cargar, repetir cargas, verificar herramientas y borrar datos. Un contrato de comandos hace cada accion testeable de forma independiente.

**Alternatives considered**:
- Un unico comando interactivo: descartado porque dificulta automatizacion y pruebas.
- UI web: fuera de alcance de esta feature.

## Decision: Validacion local antes de escribir o borrar

**Rationale**: Si el stack o las herramientas no estan disponibles, la carga debe fallar antes de dejar datos parciales. La validacion evita estados inconsistentes.

**Alternatives considered**:
- Intentar escribir y reportar errores al final: descartado por riesgo de cargas incompletas.

## Decision: Integracion con PostgreSQL y VictoriaMetrics existentes

**Rationale**: Los dashboards actuales dependen de catalogo/capacity en PostgreSQL y metricas en VictoriaMetrics. El generador debe poblar o validar ambos destinos para demostrar interconexion.

**Alternatives considered**:
- Solo datos SQL: insuficiente para dashboards tecnicos basados en series.
- Solo metricas: insuficiente para catalogo, riesgos y recomendaciones.
