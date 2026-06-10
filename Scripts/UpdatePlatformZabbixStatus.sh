#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

StatusDir="$REPO_ROOT/.capacity-test-data/ZabbixAgent"
StatusFile="$StatusDir/PlatformStatus.tsv"
MetricFile="$StatusDir/PlatformMetrics.tsv"

mkdir -p "$StatusDir"

NormalizePercent() {
  printf '%s\n' "${1:-0}" | tr -d '%' | awk '{ if ($1 == "") print "0"; else print $1 + 0 }'
}

NormalizeBytes() {
  RawValue="${1:-0}"
  printf '%s\n' "$RawValue" | awk '
    function multiplier(Unit) {
      Unit = tolower(Unit)
      if (Unit == "kb" || Unit == "kib") return 1024
      if (Unit == "mb" || Unit == "mib") return 1024 * 1024
      if (Unit == "gb" || Unit == "gib") return 1024 * 1024 * 1024
      if (Unit == "tb" || Unit == "tib") return 1024 * 1024 * 1024 * 1024
      return 1
    }
    {
      Value = $1 + 0
      Unit = $1
      gsub(/[0-9.]/, "", Unit)
      if (Unit == "" && $2 != "") Unit = $2
      printf "%.0f\n", Value * multiplier(Unit)
    }
  '
}

ContainerMetricLine() {
  Service="$1"
  Container="$(ContainerFor "$Service")"
  CpuPercent="0"
  MemoryUsedBytes="0"
  MemoryPercent="0"
  NetworkInputBytes="0"
  NetworkOutputBytes="0"
  BlockInputBytes="0"
  BlockOutputBytes="0"

  if [ "$STACK_DRY_RUN" != "1" ] && "$PODMAN_BIN" container exists "$Container" >/dev/null 2>&1 && [ "$("$PODMAN_BIN" inspect -f '{{.State.Running}}' "$Container")" = "true" ]; then
    StatsLine="$("$PODMAN_BIN" stats --no-stream --format '{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}' "$Container" 2>/dev/null || true)"
    if [ -n "$StatsLine" ]; then
      CpuRaw="$(printf '%s\n' "$StatsLine" | awk -F '	' '{print $1}')"
      MemoryRaw="$(printf '%s\n' "$StatsLine" | awk -F '	' '{print $2}')"
      MemoryPercentRaw="$(printf '%s\n' "$StatsLine" | awk -F '	' '{print $3}')"
      NetworkRaw="$(printf '%s\n' "$StatsLine" | awk -F '	' '{print $4}')"
      BlockRaw="$(printf '%s\n' "$StatsLine" | awk -F '	' '{print $5}')"
      CpuPercent="$(NormalizePercent "$CpuRaw")"
      MemoryUsedBytes="$(NormalizeBytes "$(printf '%s\n' "$MemoryRaw" | awk -F ' / ' '{print $1}')")"
      MemoryPercent="$(NormalizePercent "$MemoryPercentRaw")"
      NetworkInputBytes="$(NormalizeBytes "$(printf '%s\n' "$NetworkRaw" | awk -F ' / ' '{print $1}')")"
      NetworkOutputBytes="$(NormalizeBytes "$(printf '%s\n' "$NetworkRaw" | awk -F ' / ' '{print $2}')")"
      BlockInputBytes="$(NormalizeBytes "$(printf '%s\n' "$BlockRaw" | awk -F ' / ' '{print $1}')")"
      BlockOutputBytes="$(NormalizeBytes "$(printf '%s\n' "$BlockRaw" | awk -F ' / ' '{print $2}')")"
    fi
  fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$Container" "$CpuPercent" "$MemoryUsedBytes" "$MemoryPercent" \
    "$NetworkInputBytes" "$NetworkOutputBytes" "$BlockInputBytes" "$BlockOutputBytes" \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}

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

{
  echo "HostName	CpuPercent	MemoryUsedBytes	MemoryPercent	NetworkInputBytes	NetworkOutputBytes	BlockInputBytes	BlockOutputBytes	UpdatedAt"
  for Service in $STACK_SERVICES; do
    ContainerMetricLine "$Service"
  done
} > "$MetricFile"

Info "estado de plataforma actualizado para Zabbix Agent: $StatusFile"
Info "metricas de plataforma actualizadas para Zabbix Agent: $MetricFile"
