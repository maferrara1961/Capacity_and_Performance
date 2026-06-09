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
```

Los servicios permitidos son: PostgreSQL, VictoriaMetrics, Zabbix, Grafana y CapacityEngine.
