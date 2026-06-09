#!/usr/bin/env bash

set -eu

PROJECT_NAME="capacity-performance"
STACK_NETWORK="${PROJECT_NAME}-net"
DEFAULT_VERSION="${STACK_VERSION:-latest}"
STACK_DRY_RUN="${STACK_DRY_RUN:-0}"
PODMAN_BIN="${PODMAN_BIN:-podman}"

STACK_SERVICES="PostgreSQL VictoriaMetrics ZabbixServer ZabbixWeb Grafana CapacityEngine"
STACK_START_ORDER="PostgreSQL VictoriaMetrics ZabbixServer ZabbixWeb Grafana CapacityEngine"
STACK_STOP_ORDER="CapacityEngine Grafana ZabbixWeb ZabbixServer VictoriaMetrics PostgreSQL"

FindRepoRoot() {
  CurrentDir="$(pwd)"
  while [ "$CurrentDir" != "/" ]; do
    if [ -f "$CurrentDir/Config/StackManifest.yml" ] && [ -d "$CurrentDir/ContainerImages" ]; then
      printf '%s\n' "$CurrentDir"
      return 0
    fi
    CurrentDir="$(dirname "$CurrentDir")"
  done
  echo "ERROR: no se pudo resolver la raiz del repositorio" >&2
  return 1
}

REPO_ROOT="${REPO_ROOT:-$(FindRepoRoot)}"

Info() {
  echo "INFO: $*"
}

Error() {
  echo "ERROR: $*" >&2
}

IsAllowedService() {
  case "${1:-}" in
    PostgreSQL|VictoriaMetrics|Zabbix|ZabbixServer|ZabbixWeb|Grafana|CapacityEngine) return 0 ;;
    *) return 1 ;;
  esac
}

RequireService() {
  Service="${1:-}"
  if ! IsAllowedService "$Service"; then
    Error "servicio no permitido: ${Service:-vacio}"
    Error "servicios permitidos: $STACK_SERVICES"
    return 1
  fi
}

RequireVersion() {
  Version="${1:-}"
  if [ -z "$Version" ]; then
    Error "la version no puede estar vacia"
    return 1
  fi
}

RequirePositiveLines() {
  Lines="${1:-}"
  case "$Lines" in
    ''|*[!0-9]*|0)
      Error "la cantidad de lineas debe ser un numero positivo"
      return 1
      ;;
  esac
}

ContainerfileFor() {
  Service="$1"
  RequireService "$Service"
  case "$Service" in
    Zabbix) Directory="ZabbixWeb" ;;
    *) Directory="$Service" ;;
  esac
  printf '%s\n' "$REPO_ROOT/ContainerImages/$Directory/Containerfile"
}

ImageFor() {
  Service="$1"
  Version="${2:-$DEFAULT_VERSION}"
  RequireService "$Service"
  RequireVersion "$Version"
  case "$Service" in
    PostgreSQL) Suffix="postgresql" ;;
    VictoriaMetrics) Suffix="victoriametrics" ;;
    Zabbix|ZabbixWeb) Suffix="zabbix-web" ;;
    ZabbixServer) Suffix="zabbix-server" ;;
    Grafana) Suffix="grafana" ;;
    CapacityEngine) Suffix="capacity-engine" ;;
  esac
  printf 'localhost/%s-%s:%s\n' "$PROJECT_NAME" "$Suffix" "$Version"
}

ContainerFor() {
  RequireService "$1"
  case "$1" in
    PostgreSQL) echo "${PROJECT_NAME}-postgresql" ;;
    VictoriaMetrics) echo "${PROJECT_NAME}-victoriametrics" ;;
    Zabbix|ZabbixWeb) echo "${PROJECT_NAME}-zabbix-web" ;;
    ZabbixServer) echo "${PROJECT_NAME}-zabbix-server" ;;
    Grafana) echo "${PROJECT_NAME}-grafana" ;;
    CapacityEngine) echo "${PROJECT_NAME}-capacity-engine" ;;
  esac
}

PortArgsFor() {
  RequireService "$1"
  case "$1" in
    PostgreSQL) echo "-p 5432:5432" ;;
    VictoriaMetrics) echo "-p 8428:8428" ;;
    Zabbix|ZabbixWeb) echo "-p 8080:8080" ;;
    ZabbixServer) echo "-p 10051:10051" ;;
    Grafana) echo "-p 3000:3000" ;;
    CapacityEngine) echo "" ;;
  esac
}

VolumeArgsFor() {
  RequireService "$1"
  case "$1" in
    PostgreSQL) echo "-v ${PROJECT_NAME}-postgresql-data:/var/lib/postgresql/data" ;;
    VictoriaMetrics) echo "-v ${PROJECT_NAME}-victoriametrics-data:/victoria-metrics-data" ;;
    ZabbixServer) echo "-v ${PROJECT_NAME}-zabbix-server-data:/var/lib/zabbix" ;;
    Zabbix|ZabbixWeb) echo "" ;;
    Grafana) echo "-v ${PROJECT_NAME}-grafana-data:/var/lib/grafana" ;;
    CapacityEngine) echo "" ;;
  esac
}

EnvironmentArgsFor() {
  RequireService "$1"
  case "$1" in
    PostgreSQL) echo "-e POSTGRES_DB=capacity -e POSTGRES_USER=capacity -e POSTGRES_PASSWORD=capacity" ;;
    ZabbixServer) echo "-e DB_SERVER_HOST=${PROJECT_NAME}-postgresql -e POSTGRES_DB=capacity -e POSTGRES_USER=capacity -e POSTGRES_PASSWORD=capacity" ;;
    Zabbix|ZabbixWeb) echo "-e ZBX_SERVER_HOST=${PROJECT_NAME}-zabbix-server -e DB_SERVER_HOST=${PROJECT_NAME}-postgresql -e POSTGRES_DB=capacity -e POSTGRES_USER=capacity -e POSTGRES_PASSWORD=capacity" ;;
    Grafana) echo "-e GF_SECURITY_ADMIN_USER=admin -e GF_SECURITY_ADMIN_PASSWORD=admin" ;;
    VictoriaMetrics|CapacityEngine) echo "" ;;
  esac
}

DependenciesFor() {
  RequireService "$1"
  case "$1" in
    PostgreSQL|VictoriaMetrics) echo "" ;;
    ZabbixServer) echo "PostgreSQL" ;;
    Zabbix|ZabbixWeb) echo "PostgreSQL ZabbixServer" ;;
    Grafana) echo "PostgreSQL VictoriaMetrics" ;;
    CapacityEngine) echo "PostgreSQL VictoriaMetrics" ;;
  esac
}

IsBatchService() {
  RequireService "$1"
  case "$1" in
    CapacityEngine) return 0 ;;
    *) return 1 ;;
  esac
}

RequireRuntime() {
  if [ "$STACK_DRY_RUN" = "1" ]; then
    Info "modo simulacion activo; no se requiere Podman"
    return 0
  fi
  if ! command -v "$PODMAN_BIN" >/dev/null 2>&1; then
    Error "Podman no esta disponible para el usuario actual"
    return 1
  fi
}

RequireContainerfile() {
  FilePath="$(ContainerfileFor "$1")"
  if [ ! -f "$FilePath" ]; then
    Error "falta Containerfile requerido: $FilePath"
    return 1
  fi
}

RequireAllContainerfiles() {
  for Service in $STACK_SERVICES; do
    RequireContainerfile "$Service"
  done
}

ImageExists() {
  Service="$1"
  Version="${2:-$DEFAULT_VERSION}"
  Image="$(ImageFor "$Service" "$Version")"
  if [ "$STACK_DRY_RUN" = "1" ]; then
    Info "imagen local validada: $Image"
    return 0
  fi
  "$PODMAN_BIN" image exists "$Image" >/dev/null 2>&1
}

RequireImage() {
  Service="$1"
  Version="${2:-$DEFAULT_VERSION}"
  Image="$(ImageFor "$Service" "$Version")"
  if ! ImageExists "$Service" "$Version"; then
    Error "falta la imagen local requerida: $Image"
    Error "construya las imagenes antes de iniciar: Scripts/BuildImages.sh"
    return 1
  fi
}

RequireAllImages() {
  for Service in $STACK_SERVICES; do
    RequireImage "$Service" "$DEFAULT_VERSION"
  done
}

RunPodman() {
  if [ "$STACK_DRY_RUN" = "1" ]; then
    echo "SIMULACION: $PODMAN_BIN $*"
    return 0
  fi
  "$PODMAN_BIN" "$@"
}

EnsureNetwork() {
  RequireRuntime
  if [ "$STACK_DRY_RUN" = "1" ]; then
    Info "red comun validada: $STACK_NETWORK"
    RunPodman network create "$STACK_NETWORK"
    return 0
  fi
  if "$PODMAN_BIN" network exists "$STACK_NETWORK" >/dev/null 2>&1; then
    Info "red comun existente: $STACK_NETWORK"
  else
    Info "creando red comun: $STACK_NETWORK"
    "$PODMAN_BIN" network create "$STACK_NETWORK" >/dev/null
  fi
}
