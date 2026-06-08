#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

Service="${1:-}"
if [ "$#" -ge 2 ]; then
  Version="$2"
else
  Version="$DEFAULT_VERSION"
fi

BuildOne() {
  BuildService="$1"
  BuildVersion="$2"
  RequireContainerfile "$BuildService"
  Image="$(ImageFor "$BuildService" "$BuildVersion")"
  Containerfile="$(ContainerfileFor "$BuildService")"
  Info "construyendo imagen $Image desde $Containerfile"
  RunPodman build -t "$Image" -f "$Containerfile" "$REPO_ROOT"
}

RequireRuntime

Built=0
Failed=0

if [ -z "$Service" ]; then
  RequireAllContainerfiles
  for Item in $STACK_SERVICES; do
    if BuildOne "$Item" "$Version"; then
      Built=$((Built + 1))
    else
      Failed=$((Failed + 1))
    fi
  done
else
  RequireService "$Service"
  RequireVersion "$Version"
  if BuildOne "$Service" "$Version"; then
    Built=1
  else
    Failed=1
  fi
fi

Info "resumen de build: construidas=$Built fallidas=$Failed"
[ "$Failed" -eq 0 ]
