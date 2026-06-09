#!/usr/bin/env bash
set -eu

RequiredFiles="
Config/StackManifest.yml
Config/PodmanStack.yml
ARCH.md
ContainerImages/ZabbixServer/Containerfile
ContainerImages/ZabbixWeb/Containerfile
ContainerImages/VictoriaMetrics/Containerfile
ContainerImages/Grafana/Containerfile
ContainerImages/PostgreSQL/Containerfile
ContainerImages/CapacityEngine/Containerfile
Scripts/StackCommon.sh
Scripts/BuildImages.sh
Scripts/StartStack.sh
Scripts/StopStack.sh
Scripts/StackLogs.sh
Scripts/StackStatus.sh
Scripts/CleanupStack.sh
Scripts/ValidateLocalAccess.sh
Scripts/ManageTestData.sh
Scripts/GenerateVerificationBatches.sh
Scripts/GenerateHistoricalVerificationBatches.sh
Config/Grafana/Datasources/Datasources.yml
Config/Grafana/DashboardProviders/Provisioning.yml
Config/Grafana/Dashboards/ExecutiveCapacityDashboard.json
Config/Grafana/Dashboards/TechnicalPerformanceDashboard.json
Config/Grafana/Dashboards/CapacityPlanningDashboard.json
Config/Grafana/Dashboards/ApplicationDashboard.json
Sql/Schema/001_Catalog.sql
Sql/Schema/002_CapacityOutputs.sql
Sql/Schema/003_TestDataLoads.sql
Sql/Seed/SampleCatalog.sql
"

for FilePath in $RequiredFiles; do
  if [ ! -f "$FilePath" ]; then
    echo "Falta archivo requerido: $FilePath" >&2
    exit 1
  fi
done

if grep -R "pip install\\|requirements.txt\\|poetry\\|pipenv" CapacityEngine ContainerImages/CapacityEngine Config/StackManifest.yml >/dev/null 2>&1; then
  echo "Dependencia de codigo de aplicacion no aprobada detectada" >&2
  exit 1
fi

if ! grep -q "http://capacity-performance-victoriametrics:8428" Config/Grafana/Datasources/Datasources.yml; then
  echo "Datasource VictoriaMetrics no apunta al contenedor esperado" >&2
  exit 1
fi

if ! grep -q "uid: VictoriaMetrics" Config/Grafana/Datasources/Datasources.yml; then
  echo "Datasource VictoriaMetrics no declara UID estable" >&2
  exit 1
fi

if ! grep -q "capacity-performance-postgresql:5432" Config/Grafana/Datasources/Datasources.yml; then
  echo "Datasource PostgreSQL no apunta al contenedor esperado" >&2
  exit 1
fi

if ! grep -q "uid: CapacityPostgreSQL" Config/Grafana/Datasources/Datasources.yml; then
  echo "Datasource PostgreSQL no declara UID estable" >&2
  exit 1
fi

if ! grep -A8 "uid: CapacityPostgreSQL" Config/Grafana/Datasources/Datasources.yml | grep -q "database: capacity"; then
  echo "Datasource PostgreSQL no declara base por defecto capacity" >&2
  exit 1
fi

if ! grep -R "CapacityPostgreSQL" Config/Grafana/Dashboards/*.json >/dev/null 2>&1; then
  echo "Dashboards no declaran datasource PostgreSQL explicito" >&2
  exit 1
fi

if ! grep -R "VictoriaMetrics" Config/Grafana/Dashboards/*.json >/dev/null 2>&1; then
  echo "Dashboards no declaran datasource VictoriaMetrics explicito" >&2
  exit 1
fi

if ! grep -R '"name": "LoadId"' Config/Grafana/Dashboards/*.json >/dev/null 2>&1; then
  echo "Dashboards no declaran filtro de lote LoadId" >&2
  exit 1
fi

if ! grep -R 'load_id=~\\"${LoadId:regex}\\"' Config/Grafana/Dashboards/*.json >/dev/null 2>&1; then
  echo "Dashboards no filtran series VictoriaMetrics por lote" >&2
  exit 1
fi

for ExpectedText in "Top 5 Capacity Risks" "Top Consumers And Outliers" "Overprovisioned Resources" "Service Capacity Risk"; do
  if ! grep -R "$ExpectedText" Config/Grafana/Dashboards/*.json >/dev/null 2>&1; then
    echo "Falta panel optimizado requerido: $ExpectedText" >&2
    exit 1
  fi
done

for ExpectedSignal in "Forecast30Days" "Forecast60Days" "Forecast90Days" "P95Utilization" "synthetic_saturation"; do
  if ! grep -R "$ExpectedSignal" Config/Grafana/Dashboards/*.json >/dev/null 2>&1; then
    echo "Falta senal requerida en dashboards: $ExpectedSignal" >&2
    exit 1
  fi
done

if ! grep -q "ZBX_SERVER_HOST=.*zabbix-server" Scripts/StackCommon.sh; then
  echo "Zabbix Web no declara conexion con Zabbix Server" >&2
  exit 1
fi

if [ "${1:-}" = "--load-sample-data" ]; then
  echo "Datos de ejemplo disponibles en Sql/Seed/SampleCatalog.sql"
fi

echo "Validacion del stack completada correctamente"
