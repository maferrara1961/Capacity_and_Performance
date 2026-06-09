# Plan de Implementacion: Plataforma Enterprise de Gobierno

**Rama**: `main` | **Fecha**: 2026-06-09 | **Spec**: [spec.md](./spec.md)

**Entrada**: Especificacion desde `specs/005-enterprise-governance-platform/spec.md`

## Resumen

Extender Capacity_and_Performance desde un stack de observabilidad de capacidad y performance hacia
una plataforma enterprise de gobierno tecnologico. La implementacion agregara modelos de dominio y
flujos de evaluacion basados en evidencia para inventario tecnologico, capacidad, performance,
disponibilidad, ciclo de vida, cumplimiento, confianza de monitoreo, registro de riesgos, scoring y
dashboards ejecutivos/operativos.

El enfoque tecnico preserva el stack Podman actual y la estructura Clean Architecture: la politica
de dominio y scoring vive en `CapacityEngine/Domain` y `CapacityEngine/Application`, el acceso a
sistemas fuente queda en adapters, los datasets de reporting quedan en PostgreSQL, la evidencia de
series temporales queda en VictoriaMetrics, el inventario y monitoreo quedan gobernados por Zabbix,
y Grafana sigue siendo la capa de visualizacion.

## Contexto Tecnico

**Lenguaje/Version**: Python 3.11 para runtime de CapacityEngine; scripts shell para
administracion del stack; provisioning JSON/YAML para Grafana y Podman.

**Dependencias Primarias**: Solo APIs existentes del runtime/plataforma. Sin nuevas librerias
externas de Python, SDKs, paquetes, servicios alojados ni componentes propietarios licenciados.

**Storage**: Base PostgreSQL `capacity` para inventario, ciclo de vida, cumplimiento, riesgo,
scoring y datasets de reporting; VictoriaMetrics para evidencia historica de metricas;
Zabbix/PostgreSQL para evidencia de monitoreo e inventario; SQLite de Grafana solo para estado
interno de Grafana.

**Testing**: Suite existente stdlib `unittest` ejecutada con `Scripts/RunTests.sh`, con pruebas
unitarias, contract e integracion bajo `Tests/`.

**Plataforma Objetivo**: Stack Linux/Podman self-hosted, validado localmente y en hosts Ubuntu
remotos.

**Tipo de Proyecto**: Plataforma self-hosted de observabilidad/gobierno con motor batch Python,
scripts shell de administracion, dashboards Grafana y servicios containerizados.

**Objetivos de Performance**: Soportar 10.000+ componentes monitoreados, retencion historica
multi-anual y comprension ejecutiva del estado en sesenta segundos.

**Restricciones**: No inferir salud desde evidencia faltante; todos los scores deben estar en rango
0-100 y ser trazables; dashboards/comandos protegidos requieren autenticacion; las entradas de
usuario deben validarse; los simbolos definidos por el proyecto usan PascalCase salvo excepciones
por convenciones externas documentadas.

**Escala/Alcance**: Dominios tecnologicos enterprise: infraestructura, sistemas operativos, bases
de datos, middleware, plataformas de contenedores, plataformas de mensajeria, monitoreo,
aplicaciones enterprise y servicios de negocio.

**Dominios Tecnologicos Afectados**: Capacidad, Performance, Disponibilidad, Ciclo de Vida,
Cumplimiento y Gobierno de Monitoreo.

**Fuentes de Evidencia**: Monitoreo/inventario/eventos de Zabbix, metricas historicas de
VictoriaMetrics, datasets de metadata/inventario/ciclo de vida/cumplimiento/riesgo de PostgreSQL,
presentacion en Grafana y datasets generados de validacion.

**Salidas de Evaluacion**: Capacity Risk Assessment, Performance Risk Assessment, Availability Risk
Assessment, Lifecycle Risk Assessment, Compliance Risk Assessment, Monitoring Confidence
Assessment, Technology Health Score, registros de riesgo y dashboards ejecutivos/operativos.

## Chequeo de Constitucion

*GATE: Debe pasar antes de Phase 0 research. Re-chequear despues de Phase 1 design.*

- **TDD**: PASS. El plan requiere pruebas unitarias/contract/integracion fallidas antes de
  implementar estados de evidencia, scoring, registro de riesgos, acceso protegido y contratos de
  datos de dashboards.
- **SOLID / Clean Architecture**: PASS. Modelos de dominio y politica de scoring quedan
  independientes de Zabbix, VictoriaMetrics, PostgreSQL, Grafana, shell y adapters Podman.
- **DRY / YAGNI**: PASS. Reutiliza capas existentes de `CapacityEngine`, mecanismos de datos
  sinteticos y provisioning de dashboards; evita integraciones especulativas fuera de los dominios
  enterprise declarados.
- **PascalCase**: PASS. Nuevos simbolos Python, nombres de entidades y artefactos definidos por el
  proyecto usan PascalCase; labels externos de metricas y convenciones JSON de Grafana quedan como
  excepciones documentadas.
- **Sin Nuevas Librerias Externas**: PASS. La implementacion usa Python stdlib, shell existente,
  imagenes Podman existentes y APIs de plataforma aprobadas.
- **Validacion y Auth**: PASS. Entradas de scripts, filtros de dashboard, actualizaciones de
  gobierno, cambios de inventario y comandos de registro de riesgos deben validarse; vistas de
  Grafana y Zabbix permanecen autenticadas.
- **Alcance de Plataforma**: PASS. El modelo representa dominio y tipo tecnologico como datos para
  permitir agregar tecnologias futuras sin redisenar la politica de evaluacion.
- **Manejo de Evidencia**: PASS. Los estados incluyen disponible, faltante, desconocida, incompleta
  y no verificada; la evidencia faltante no puede producir estado saludable.
- **Logica de Riesgo y Tendencia**: PASS. Criterios de riesgo y scoring son objetivos,
  reproducibles y trazables; los forecasts requieren evidencia historica y deben mostrar estados de
  evidencia insuficiente.
- **Scoring**: PASS. Todos los scores de dominio y Technology Health Score usan rango 0-100 con
  umbrales de clasificacion definidos por la especificacion.
- **Soporte a Decision Humana**: PASS. Las recomendaciones identifican tecnologias/servicios
  afectados y soportan decisiones humanas sin remediacion automatica.

## Estructura del Proyecto

### Documentacion (este feature)

```text
specs/005-enterprise-governance-platform/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── cli-contract.md
│   ├── dashboard-contract.md
│   └── dataset-contract.md
└── checklists/
    └── requirements.md
```

### Codigo Fuente (raiz del repositorio)

```text
CapacityEngine/
├── Domain/              # Politica de inventario, evidencia, score, riesgo y recomendacion
├── Application/         # Evaluacion, scoring, orquestacion, validacion y casos de uso
├── Adapters/            # Adapters PostgreSQL, VictoriaMetrics, Zabbix y comandos
└── Scheduler/           # Entrypoints batch y comandos CLI

Config/
├── Grafana/
│   ├── Dashboards/      # Vistas ejecutivas, operativas, planning, aplicacion y gobierno
│   ├── Datasources/
│   └── DashboardProviders/
├── PodmanStack.yml
└── StackManifest.yml

Scripts/                 # Build/start/stop/status/logs/sync/load/validate
Tests/
├── Unit/
├── Contract/
└── Integration/
docs/
```

**Decision de Estructura**: Usar el layout existente de plataforma en un solo repositorio. La
expansion de dominio se implementara dentro de `CapacityEngine` y las carpetas existentes de
configuracion/scripts para que gobierno comparta el mismo stack, validacion y modelo de despliegue
que la plataforma actual de capacidad.

## Seguimiento de Complejidad

No se planifican violaciones de constitucion.

| Violacion | Por que se necesita | Alternativa simple rechazada porque |
|-----------|---------------------|-------------------------------------|
