#!/usr/bin/env bash
set -eu

. "$(dirname "$0")/StackCommon.sh"

Action="${1:-install}"
StartMarker="# CAPACITY_PLATFORM_METRICS_START"
EndMarker="# CAPACITY_PLATFORM_METRICS_END"
CronLine="* * * * * cd \"$REPO_ROOT\" && \"$REPO_ROOT/Scripts/UpdatePlatformZabbixStatus.sh\" >/dev/null 2>&1"

CurrentCrontab() {
  crontab -l 2>/dev/null || true
}

WithoutManagedBlock() {
  awk -v StartMarker="$StartMarker" -v EndMarker="$EndMarker" '
    $0 == StartMarker {
      Skip = 1
      next
    }
    $0 == EndMarker {
      Skip = 0
      next
    }
    Skip != 1 {
      print
    }
  '
}

case "$Action" in
  install)
    {
      CurrentCrontab | WithoutManagedBlock
      echo "$StartMarker"
      echo "$CronLine"
      echo "$EndMarker"
    } | crontab -
    Info "cron de metricas de plataforma instalado para ejecutar cada minuto"
    ;;
  remove)
    CurrentCrontab | WithoutManagedBlock | crontab -
    Info "cron de metricas de plataforma removido"
    ;;
  status)
    if CurrentCrontab | grep -q "$StartMarker"; then
      Info "cron de metricas de plataforma instalado"
      CurrentCrontab | sed -n "/$StartMarker/,/$EndMarker/p"
    else
      Info "cron de metricas de plataforma no instalado"
    fi
    ;;
  *)
    Error "accion no permitida: $Action"
    Error "acciones permitidas: install remove status"
    exit 1
    ;;
esac
