# Administracion de Imagenes y Stack

Todos los comandos muestran mensajes en castellano y validan entradas antes de operar sobre
contenedores.

## Build

Construir todas las imagenes:

```bash
Scripts/BuildImages.sh
```

Construir una imagen individual:

```bash
Scripts/BuildImages.sh Grafana v1.0.0
```

## Start

```bash
Scripts/StartStack.sh
Scripts/RegisterPlatformHosts.sh
```

El arranque requiere que las imagenes locales ya existan. Si falta alguna imagen, el script se
detiene antes de crear contenedores y solicita ejecutar `Scripts/BuildImages.sh`. Luego usa la red
comun del stack e inicia servicios en orden compatible con dependencias: PostgreSQL,
VictoriaMetrics, Zabbix, Grafana y CapacityEngine.

`Scripts/RegisterPlatformHosts.sh` registra los servidores de la plataforma en Zabbix dentro del
grupo `Capacity Platform`, todos con ambiente `Produccion`: PostgreSQL, VictoriaMetrics,
ZabbixServer, ZabbixWeb, ZabbixAgent, Grafana y CapacityEngine.

Los componentes con puerto usan items TCP `net.tcp.service[...]`. `CapacityEngine`, al ser batch,
usa `capacity.platform.status[...]` expuesto por ZabbixAgent desde
`.capacity-test-data/ZabbixAgent/PlatformStatus.tsv`.

Cada componente tambien expone metricas por contenedor desde `podman stats`:
`CpuPercent`, `MemoryUsedBytes`, `MemoryPercent`, `NetworkInputBytes`, `NetworkOutputBytes`,
`BlockInputBytes` y `BlockOutputBytes`. `Scripts/UpdatePlatformZabbixStatus.sh` actualiza
`.capacity-test-data/ZabbixAgent/PlatformMetrics.tsv`; para historico continuo debe ejecutarse cada
minuto con cron o systemd timer del usuario `opc`.

Grafana monta la configuracion de `Config/Grafana` directamente desde el repositorio. Los providers
de dashboard y los JSON de dashboard se montan en rutas separadas para evitar que Grafana lea el
provider como dashboard. Despues de un `git pull`, ejecutar `Scripts/StopStack.sh` y
`Scripts/StartStack.sh` reprovisiona dashboards y datasources sin reconstruir la imagen.

## Modo de uso

URLs locales luego de iniciar el stack:

```text
Grafana:          http://localhost:3000
Zabbix Web:       http://localhost:8080
VictoriaMetrics:  http://localhost:8428
PostgreSQL:       localhost:5432
Zabbix Server:    localhost:10051
```

Credenciales por defecto para Grafana:

```text
Usuario: admin
Password: admin
```

Credenciales por defecto para Zabbix Web:

```text
Usuario: Admin
Password: zabbix
```

En servidores remotos, reemplazar `localhost` por la IP publica o nombre DNS del servidor. Tambien
se deben habilitar los puertos en el firewall local y en las reglas de red del proveedor cloud.

PostgreSQL y Zabbix Server no son servicios HTTP. Un `curl` contra `localhost:5432` puede devolver
respuesta vacia, y eso no indica una falla de PostgreSQL.

Validar acceso local con HTTP para interfaces web y TCP para servicios no HTTP:

```bash
Scripts/ValidateLocalAccess.sh
Scripts/ValidateLocalAccess.sh IP_DEL_SERVIDOR
```

Generar y validar datos sinteticos para dashboards:

```bash
Scripts/ManageTestData.sh load --profile mixed --volume small
Scripts/ManageTestData.sh list
Scripts/ManageTestData.sh validate
Scripts/ManageTestData.sh delete --all --confirmar
```

Generar lotes de verificacion para Grafana, VictoriaMetrics, PostgreSQL y Zabbix:

```bash
Scripts/GenerateVerificationBatches.sh DemoFull001
```

Generar historia diaria de 30, 60 y 90 dias para validar tendencias y forecast:

```bash
Scripts/GenerateHistoricalVerificationBatches.sh HistoryFull001
```

En Grafana usar el filtro `Lote`; `All` muestra todos los lotes cargados. En Zabbix revisar los
hosts del grupo `Capacity Synthetic`, sus graficos `Capacity Synthetic - <host>` y los triggers
Warning/Critical generados por metrica.

Para dashboards optimizados, revisar en Grafana las carpetas `Capacity`, `Performance` y
`Risk & Compliance`:

- Cada dashboard comienza con `Como leer este dashboard`, que explica que muestra cada vista, como
  interpretar los cuadros y que accion tomar.
- `Capacity`: decision ejecutiva, planificacion, trends, forecast y top consumers.
- `Performance`: diagnostico operativo, metricas tecnicas, aplicaciones y performance end-to-end.
- `Risk & Compliance`: salud enterprise, gobierno, licencias, compliance y software backlevel.

Si Grafana muestra dashboards tecnicos duplicados, conservar solo el dashboard con UID
`technical-performance`:

```bash
Scripts/CleanupGrafanaDashboards.sh
Scripts/CleanupGrafanaDashboards.sh --confirmar
Scripts/StopStack.sh
Scripts/StartStack.sh
```

Si Grafana muestra que PostgreSQL no tiene base por defecto configurada, actualizar el repositorio y
reiniciar el stack para reprovisionar `CapacityPostgreSQL` con `jsonData.database=capacity`:

```bash
git pull
Scripts/StopStack.sh
Scripts/StartStack.sh
```

En Zabbix ingresar con `Admin` / `zabbix` y revisar `Monitoring > Latest data` filtrando por el
grupo `Capacity Synthetic`.

## Stop

```bash
Scripts/StopStack.sh
```

Stop detiene contenedores administrados y preserva volumenes persistentes.

## Cleanup

```bash
Scripts/CleanupStack.sh --confirmar
```

Cleanup elimina contenedores y red temporal administrada. No elimina volumenes persistentes por
defecto.

## Logs y Estado

```bash
Scripts/StackLogs.sh Grafana 100
Scripts/StackStatus.sh
Scripts/StackStatus.sh Grafana
Scripts/StackStatus.sh CapacityEngine
```

`CapacityEngine` es una tarea batch. Cuando finaliza con exit code `0`, el estado esperado es
`salud: completado correctamente`.

Los servicios permitidos son: PostgreSQL, VictoriaMetrics, ZabbixServer, ZabbixWeb, Grafana y
CapacityEngine. `Zabbix` se conserva como alias operativo de `ZabbixWeb`.
