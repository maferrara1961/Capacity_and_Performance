#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

Service="${1:-}"
Overall=0

RequireRuntime

StatusOne() {
  StatusService="$1"
  RequireService "$StatusService"
  Container="$(ContainerFor "$StatusService")"
  Ports="$(PortArgsFor "$StatusService")"
  Deps="$(DependenciesFor "$StatusService")"
  Info "estado de $StatusService"
  echo "  contenedor: $Container"
  echo "  red: $STACK_NETWORK"
  echo "  puertos: ${Ports:-sin puertos publicados}"
  echo "  dependencias: ${Deps:-sin dependencias}"
  if [ "$STACK_DRY_RUN" = "1" ]; then
    echo "  salud: saludable (simulacion)"
    return 0
  fi
  if "$PODMAN_BIN" container exists "$Container" >/dev/null 2>&1 && [ "$("$PODMAN_BIN" inspect -f '{{.State.Running}}' "$Container")" = "true" ]; then
    echo "  salud: saludable"
    return 0
  fi
  echo "  salud: detenido"
  return 1
}

if [ -z "$Service" ]; then
  for Item in $STACK_SERVICES; do
    if ! StatusOne "$Item"; then
      Overall=1
    fi
  done
else
  StatusOne "$Service" || Overall=1
fi

exit "$Overall"
