#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/StackCommon.sh"

CONFIRM="${1:-}"
GRAFANA_UID="technical-performance"
GRAFANA_TITLE="Technical Performance Dashboard"
POSTGRES_CONTAINER="$(ContainerFor PostgreSQL)"

RequireRuntime

Info "validando dashboards tecnicos persistidos en PostgreSQL/Grafana"

ListSql="
select id, uid, title, is_folder, folder_id
from dashboard
where is_folder = false
  and (title = '${GRAFANA_TITLE}' or uid = '${GRAFANA_UID}')
order by case when uid = '${GRAFANA_UID}' then 0 else 1 end, id;
"

if [ "$STACK_DRY_RUN" = "1" ]; then
  Info "modo simulacion: se listarian dashboards con titulo ${GRAFANA_TITLE}"
else
  "$PODMAN_BIN" exec "$POSTGRES_CONTAINER" psql -U capacity -d grafana -c "$ListSql"
fi

if [ "$CONFIRM" != "--confirmar" ]; then
  Info "no se realizaron cambios; para borrar duplicados ejecutar: Scripts/CleanupGrafanaDashboards.sh --confirmar"
  exit 0
fi

DeleteSql="
delete from dashboard
where is_folder = false
  and title = '${GRAFANA_TITLE}'
  and uid <> '${GRAFANA_UID}';
"

if [ "$STACK_DRY_RUN" = "1" ]; then
  Info "modo simulacion: se borrarian dashboards tecnicos duplicados con uid distinto de ${GRAFANA_UID}"
else
  "$PODMAN_BIN" exec "$POSTGRES_CONTAINER" psql -U capacity -d grafana -c "$DeleteSql"
fi

Info "limpieza de dashboards tecnicos finalizada; reiniciar Grafana para refrescar la UI"
