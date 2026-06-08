#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

Service="${1:-}"
Lines="${2:-100}"

RequireRuntime
RequirePositiveLines "$Lines"

ShowLogs() {
  LogService="$1"
  RequireService "$LogService"
  Container="$(ContainerFor "$LogService")"
  Info "mostrando ultimas $Lines lineas de $LogService"
  RunPodman logs --tail "$Lines" "$Container"
}

if [ -z "$Service" ]; then
  for Item in $STACK_SERVICES; do
    ShowLogs "$Item"
  done
else
  ShowLogs "$Service"
fi
