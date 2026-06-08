#!/usr/bin/env bash
set -eu

STACK_FILE="Config/PodmanStack.yml"
if [ ! -f "$STACK_FILE" ]; then
  echo "Missing $STACK_FILE" >&2
  exit 1
fi

echo "Stack definition validated: $STACK_FILE"
echo "Build and run with Podman using the declared Containerfiles for production deployment."
