# Contrato: Ciclo de Vida del Stack

## Proposito

Define los comandos para iniciar, detener y limpiar el stack respetando dependencias,
interconexion y persistencia.

## Comandos

```text
Scripts/StartStack.sh
Scripts/StopStack.sh
Scripts/CleanupStack.sh --confirmar
```

## Start

**Precondiciones**:
- Imagenes requeridas disponibles.
- Red comun creada o creable.
- Puertos requeridos disponibles.
- Variables requeridas presentes.

**Reglas**:
- PostgreSQL y VictoriaMetrics deben iniciar antes de los servicios que los consumen.
- Grafana debe iniciar con datasources y dashboards provisionados.
- CapacityEngine debe iniciar con acceso a PostgreSQL y VictoriaMetrics.
- Zabbix debe iniciar conectado a PostgreSQL.

## Stop

**Reglas**:
- Detiene solo contenedores administrados por el stack.
- No elimina volumenes persistentes.
- Informa servicios ya detenidos sin tratarlo como error fatal.

## Cleanup

**Reglas**:
- Requiere confirmacion explicita.
- Elimina solo recursos temporales permitidos.
- No elimina volumenes persistentes por defecto.

## Salidas Esperadas

- Mensajes en castellano.
- Resumen de servicios afectados.
- Codigo de salida distinto de cero si el stack queda no saludable.
