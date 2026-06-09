#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX="${1:-Verify$(date -u +%Y%m%d%H%M%S)}"
VOLUME="${VERIFY_VOLUME:-small}"

RunLoad() {
  Profile="$1"
  LoadId="${PREFIX}-${Profile}"
  "$SCRIPT_DIR/ManageTestData.sh" load --profile "$Profile" --volume "$VOLUME" --load-id "$LoadId"
  "$SCRIPT_DIR/ManageTestData.sh" validate --load-id "$LoadId"
}

RunLoad normal
RunLoad warning
RunLoad critical
RunLoad mixed

echo "INFO: lotes de verificacion generados"
echo "  prefijo: $PREFIX"
echo "  volumen: $VOLUME"
echo "  lotes: ${PREFIX}-normal ${PREFIX}-warning ${PREFIX}-critical ${PREFIX}-mixed"
