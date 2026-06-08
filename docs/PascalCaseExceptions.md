# PascalCase Exceptions

The project uses PascalCase for project-owned symbols and artifacts. The following exceptions are
required by platform conventions:

- Containerfile base image names use vendor-provided lowercase image references.
- Grafana dashboard JSON properties use Grafana schema field names.
- SQL object names may preserve platform and query conventions.
- Metrics labels and query strings may use external metric naming conventions.
