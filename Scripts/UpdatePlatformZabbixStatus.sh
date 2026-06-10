#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

StatusDir="$REPO_ROOT/.capacity-test-data/ZabbixAgent"
StatusFile="$StatusDir/PlatformStatus.tsv"

mkdir -p "$StatusDir"

{
  echo "HostName	Status	UpdatedAt"
  for Service in $STACK_SERVICES; do
    Container="$(ContainerFor "$Service")"
    Status="0"
    if [ "$STACK_DRY_RUN" = "1" ]; then
      Status="1"
    elif "$PODMAN_BIN" container exists "$Container" >/dev/null 2>&1; then
      if [ "$("$PODMAN_BIN" inspect -f '{{.State.Running}}' "$Container")" = "true" ]; then
        Status="1"
      elif IsBatchService "$Service" && [ "$("$PODMAN_BIN" inspect -f '{{.State.ExitCode}}' "$Container")" = "0" ]; then
        Status="1"
      fi
    fi
    printf '%s\t%s\t%s\n' "$Container" "$Status" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  done
} > "$StatusFile"

Info "estado de plataforma actualizado para Zabbix Agent: $StatusFile"
