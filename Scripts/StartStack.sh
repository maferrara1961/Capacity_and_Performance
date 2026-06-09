#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

StartOne() {
  Service="$1"
  Container="$(ContainerFor "$Service")"
  Image="$(ImageFor "$Service" "$DEFAULT_VERSION")"
  Ports="$(PortArgsFor "$Service")"
  Volumes="$(VolumeArgsFor "$Service")"
  EnvArgs="$(EnvironmentArgsFor "$Service")"
  Deps="$(DependenciesFor "$Service")"
  if [ "$Service" = "ZabbixAgent" ]; then
    mkdir -p "$REPO_ROOT/.capacity-test-data/ZabbixAgent"
  fi
  if [ -n "$Deps" ]; then
    Info "validando dependencias de $Service: $Deps"
  fi
  Info "iniciando $Service como $Container"
  # shellcheck disable=SC2086
  RunPodman run -d --pull=never --replace --name "$Container" --network "$STACK_NETWORK" $Ports $Volumes $EnvArgs "$Image"
}

EnsurePostgreSqlDatabases() {
  if [ "$STACK_DRY_RUN" = "1" ]; then
    Info "base PostgreSQL validada: capacity"
    Info "base PostgreSQL validada: grafana"
    return 0
  fi
  Container="$(ContainerFor PostgreSQL)"
  for Attempt in 1 2 3 4 5 6 7 8 9 10; do
    if "$PODMAN_BIN" exec "$Container" pg_isready -U capacity -d capacity >/dev/null 2>&1; then
      break
    fi
    sleep 2
    if [ "$Attempt" = "10" ]; then
      Error "PostgreSQL no esta listo para crear bases compartidas"
      return 1
    fi
  done
  "$PODMAN_BIN" exec -i "$Container" psql -U capacity -d capacity -v ON_ERROR_STOP=1 <<'SQL'
select 'create database grafana'
where not exists (
  select 1 from pg_database where datname = 'grafana'
)\gexec
SQL
}

RequireRuntime
RequireAllImages
EnsureNetwork

for Service in $STACK_START_ORDER; do
  StartOne "$Service"
  if [ "$Service" = "PostgreSQL" ]; then
    EnsurePostgreSqlDatabases
  fi
done

Info "stack iniciado; validar salud con Scripts/StackStatus.sh"
