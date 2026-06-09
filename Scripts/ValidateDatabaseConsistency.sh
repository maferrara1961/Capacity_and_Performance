#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

ValidateDeclaredConfiguration() {
  if ! grep -q "GF_DATABASE_TYPE=postgres" "$REPO_ROOT/Scripts/StackCommon.sh"; then
    Error "Grafana no usa PostgreSQL como motor de base de datos"
    return 1
  fi
  if ! grep -q "GF_DATABASE_NAME=grafana" "$REPO_ROOT/Scripts/StackCommon.sh"; then
    Error "Grafana no declara base grafana en PostgreSQL"
    return 1
  fi
  if grep -q "capacity-performance-grafana-data:/var/lib/grafana" "$REPO_ROOT/Scripts/StackCommon.sh"; then
    Error "Grafana conserva volumen persistente SQLite; debe persistir en PostgreSQL"
    return 1
  fi
  if ! grep -q "POSTGRES_DB=capacity" "$REPO_ROOT/Scripts/StackCommon.sh"; then
    Error "Zabbix y catalogo no declaran base PostgreSQL capacity"
    return 1
  fi
  if ! grep -q "create database grafana" "$REPO_ROOT/Sql/Init/001_CreateGrafanaDatabase.sql"; then
    Error "PostgreSQL no inicializa base grafana"
    return 1
  fi
}

ValidateRuntimeDatabase() {
  Container="$(ContainerFor PostgreSQL)"
  Query="
select 'database:capacity=' || exists(select 1 from pg_database where datname = 'capacity')
union all
select 'database:grafana=' || exists(select 1 from pg_database where datname = 'grafana')
union all
select 'table:capacity.TestLoad=' || exists(select 1 from information_schema.tables where table_schema = 'public' and table_name = 'testload')
union all
select 'table:capacity.EnterpriseTechnologyComponent=' || exists(select 1 from information_schema.tables where table_schema = 'public' and table_name = 'enterprisetechnologycomponent');
"
  "$PODMAN_BIN" exec "$Container" psql -U capacity -d capacity -tAc "$Query"
}

RequireRuntime
ValidateDeclaredConfiguration

if [ "$STACK_DRY_RUN" = "1" ]; then
  Info "consistencia declarativa PostgreSQL validada"
  Info "Grafana: PostgreSQL/grafana"
  Info "Zabbix: PostgreSQL/capacity"
  Info "Catalogo y CapacityEngine: PostgreSQL/capacity"
  exit 0
fi

RuntimeOutput="$(ValidateRuntimeDatabase)"
printf '%s\n' "$RuntimeOutput"

for Expected in \
  "database:capacity=t" \
  "database:grafana=t" \
  "table:capacity.TestLoad=t" \
  "table:capacity.EnterpriseTechnologyComponent=t"; do
  if ! printf '%s\n' "$RuntimeOutput" | grep -q "$Expected"; then
    Error "validacion PostgreSQL inconsistente: falta $Expected"
    exit 1
  fi
done

Info "consistencia PostgreSQL validada"
