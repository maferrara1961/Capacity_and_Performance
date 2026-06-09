#!/usr/bin/env bash
set -eu

STACK_DRY_RUN="${STACK_DRY_RUN:-0}"
HOST="${1:-localhost}"

Info() {
  echo "INFO: $*"
}

Error() {
  echo "ERROR: $*" >&2
}

RequireCommand() {
  CommandName="$1"
  if [ "$STACK_DRY_RUN" = "1" ]; then
    return 0
  fi
  if ! command -v "$CommandName" >/dev/null 2>&1; then
    Error "comando requerido no disponible: $CommandName"
    return 1
  fi
}

ValidateHttp() {
  Name="$1"
  Url="$2"
  Match="$3"
  Info "validando HTTP $Name en $Url"
  if [ "$STACK_DRY_RUN" = "1" ]; then
    echo "SIMULACION: curl -fsSL --max-time 5 $Url"
    return 0
  fi
  Body="$(curl -fsSL --max-time 5 "$Url")"
  if printf '%s' "$Body" | grep -qi "$Match"; then
    Info "$Name disponible"
    return 0
  fi
  Error "$Name respondio HTTP despues de seguir redirecciones, pero no contiene la marca esperada: $Match"
  return 1
}

ValidateTcp() {
  Name="$1"
  Port="$2"
  Info "validando TCP $Name en ${HOST}:${Port}"
  if [ "$STACK_DRY_RUN" = "1" ]; then
    echo "SIMULACION: conexion TCP ${HOST}:${Port}"
    return 0
  fi
  if (exec 3<>"/dev/tcp/${HOST}/${Port}") 2>/dev/null; then
    exec 3<&-
    exec 3>&-
    Info "$Name acepta conexiones TCP"
    return 0
  fi
  Error "$Name no acepta conexiones TCP en ${HOST}:${Port}"
  return 1
}

RequireCommand curl

ValidateHttp "Grafana" "http://${HOST}:3000" "grafana"
ValidateHttp "Zabbix Web" "http://${HOST}:8080" "zabbix"
ValidateHttp "VictoriaMetrics" "http://${HOST}:8428" "victoriametrics"
ValidateTcp "PostgreSQL" "5432"
ValidateTcp "Zabbix Server" "10051"

Info "validacion local de acceso completada correctamente"
