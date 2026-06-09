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
```

El arranque requiere que las imagenes locales ya existan. Si falta alguna imagen, el script se
detiene antes de crear contenedores y solicita ejecutar `Scripts/BuildImages.sh`. Luego usa la red
comun del stack e inicia servicios en orden compatible con dependencias: PostgreSQL,
VictoriaMetrics, Zabbix, Grafana y CapacityEngine.

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

En servidores remotos, reemplazar `localhost` por la IP publica o nombre DNS del servidor. Tambien
se deben habilitar los puertos en el firewall local y en las reglas de red del proveedor cloud.

PostgreSQL y Zabbix Server no son servicios HTTP. Un `curl` contra `localhost:5432` puede devolver
respuesta vacia, y eso no indica una falla de PostgreSQL.

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
