#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

if [ "${1:-}" != "--confirmar" ]; then
  Error "cleanup requiere confirmacion explicita: Scripts/CleanupStack.sh --confirmar"
  exit 1
fi

RequireRuntime

for Service in $STACK_STOP_ORDER; do
  Container="$(ContainerFor "$Service")"
  Info "eliminando contenedor temporal administrado: $Container"
  RunPodman rm -f "$Container" || Info "$Container no existia"
done

Info "eliminando red temporal si existe: $STACK_NETWORK"
RunPodman network rm "$STACK_NETWORK" || Info "la red no existia o esta en uso"
Info "cleanup finalizado; no se eliminaron volumenes persistentes"
