#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

RequireRuntime

for Service in $STACK_STOP_ORDER; do
  Container="$(ContainerFor "$Service")"
  Info "deteniendo $Service ($Container) sin borrar volumenes persistentes"
  RunPodman stop "$Container" || Info "$Service ya estaba detenido o no existe"
done

"$REPO_ROOT/Scripts/UpdatePlatformZabbixStatus.sh"
Info "stop finalizado; los volumenes persistentes fueron preservados"
