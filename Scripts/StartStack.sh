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
  if [ -n "$Deps" ]; then
    Info "validando dependencias de $Service: $Deps"
  fi
  Info "iniciando $Service como $Container"
  # shellcheck disable=SC2086
  RunPodman run -d --pull=never --replace --name "$Container" --network "$STACK_NETWORK" $Ports $Volumes $EnvArgs "$Image"
}

RequireRuntime
RequireAllImages
EnsureNetwork

for Service in $STACK_START_ORDER; do
  StartOne "$Service"
done

Info "stack iniciado; validar salud con Scripts/StackStatus.sh"
