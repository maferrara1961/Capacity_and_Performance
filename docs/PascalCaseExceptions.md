# PascalCase Exceptions

The project uses PascalCase for project-owned symbols and artifacts. The following exceptions are
required by platform conventions:

- Containerfile base image names use vendor-provided lowercase image references.
- Grafana dashboard JSON properties use Grafana schema field names.
- Grafana metric expressions and legend labels use external datasource naming conventions.
- SQL object names may preserve platform and query conventions.
- Metrics labels and query strings may use external metric naming conventions.
# Excepciones PascalCase Enterprise

Las entidades, servicios y artefactos Python definidos por el proyecto usan PascalCase. Las
excepciones enterprise aceptadas son:

- Labels de VictoriaMetrics como `load_id`, `resource_id`, `host_name` y futuros labels
  `technology_domain`, `business_service` por convencion Prometheus.
- Campos JSON/YAML de Grafana y Podman definidos por esas plataformas.
- Argumentos CLI con formato kebab-case como `--scope-id` y `--evidence-window-days`.
- Comandos shell con nombres historicos del repositorio en `Scripts/`.

Estas excepciones existen por contratos externos o convenciones operativas y no habilitan nombres
inconsistentes en codigo de dominio.
