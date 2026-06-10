#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

CurrentUser="$(id -un)"

Info "validando host Podman para el usuario $CurrentUser"

RequireRuntime

if [ "$STACK_DRY_RUN" = "1" ]; then
  Info "modo simulacion activo; preparacion de host validada"
  exit 0
fi

Info "validando version de Podman"
"$PODMAN_BIN" --version

Info "reparando locks internos de Podman si corresponde"
if "$PODMAN_BIN" system renumber >/dev/null 2>&1; then
  Info "locks de Podman validados"
else
  Error "podman system renumber reporto errores"
  Error "si el problema persiste, cerrar sesiones Podman activas y ejecutar nuevamente"
fi

if command -v loginctl >/dev/null 2>&1; then
  LingerStatus="$(loginctl show-user "$CurrentUser" -p Linger --value 2>/dev/null || true)"
  if [ "$LingerStatus" = "yes" ]; then
    Info "linger habilitado para $CurrentUser; los contenedores rootless pueden sobrevivir al cierre de SSH"
  else
    Error "linger no esta habilitado para $CurrentUser"
    Error "en servidores remotos, habilitarlo evita que systemd termine contenedores rootless al cerrar SSH"
    Error "ejecute con permisos de administrador: sudo loginctl enable-linger $CurrentUser"
    exit 1
  fi
else
  Info "loginctl no disponible; omitiendo validacion de linger"
fi

Info "host Podman validado"
