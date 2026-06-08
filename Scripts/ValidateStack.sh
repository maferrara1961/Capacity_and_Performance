#!/usr/bin/env bash
set -eu

RequiredFiles="
Config/StackManifest.yml
Config/PodmanStack.yml
ContainerImages/Zabbix/Containerfile
ContainerImages/VictoriaMetrics/Containerfile
ContainerImages/Grafana/Containerfile
ContainerImages/PostgreSQL/Containerfile
ContainerImages/CapacityEngine/Containerfile
Config/Grafana/Datasources/Datasources.yml
Config/Grafana/Dashboards/Provisioning.yml
Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json
Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json
Config/Grafana/Dashboards/CapacityPlanningDashboard.json
Config/Grafana/Dashboards/ApplicationDashboard.json
Sql/Schema/001_Catalog.sql
Sql/Schema/002_CapacityOutputs.sql
Sql/Seed/SampleCatalog.sql
"

for FilePath in $RequiredFiles; do
  if [ ! -f "$FilePath" ]; then
    echo "Missing required file: $FilePath" >&2
    exit 1
  fi
done

if grep -R "pip install\\|requirements.txt\\|poetry\\|pipenv" CapacityEngine ContainerImages/CapacityEngine Config/StackManifest.yml >/dev/null 2>&1; then
  echo "Unapproved application-code dependency detected" >&2
  exit 1
fi

if [ "${1:-}" = "--load-sample-data" ]; then
  echo "Sample data available at Sql/Seed/SampleCatalog.sql"
fi

echo "Stack validation passed"
