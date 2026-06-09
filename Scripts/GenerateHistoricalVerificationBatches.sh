#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX="${1:-History$(date -u +%Y%m%d%H%M%S)}"
VOLUME="${VERIFY_VOLUME:-small}"
PROFILES="${VERIFY_PROFILES:-normal warning critical mixed}"
WINDOWS="${VERIFY_WINDOWS:-30 60 90}"

RunHistoricalLoad() {
  Days="$1"
  Profile="$2"
  LoadId="${PREFIX}-${Days}d-${Profile}"
  "$SCRIPT_DIR/ManageTestData.sh" delete --load-id "$LoadId" >/dev/null 2>&1 || true
  "$SCRIPT_DIR/ManageTestData.sh" load --profile "$Profile" --volume "$VOLUME" --days "$Days" --load-id "$LoadId"
  "$SCRIPT_DIR/ManageTestData.sh" validate --load-id "$LoadId"
}

GeneratedLoads=""
for Days in $WINDOWS; do
  for Profile in $PROFILES; do
    RunHistoricalLoad "$Days" "$Profile"
    GeneratedLoads="${GeneratedLoads} ${PREFIX}-${Days}d-${Profile}"
  done
done

echo "INFO: lotes historicos de verificacion generados"
echo "  prefijo: $PREFIX"
echo "  volumen: $VOLUME"
echo "  ventanas: $WINDOWS"
echo "  perfiles: $PROFILES"
echo "  lotes:${GeneratedLoads}"
