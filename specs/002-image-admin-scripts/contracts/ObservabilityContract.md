# Contrato: Logs y Estado

## Proposito

Define como los operadores consultan logs y estado operativo del stack.

## Comandos

```text
Scripts/StackLogs.sh [Servicio] [Lineas]
Scripts/StackStatus.sh [Servicio]
```

## Logs

**Entradas**:
- `Servicio`: opcional. Si se omite, muestra logs del stack.
- `Lineas`: opcional. Cantidad positiva de lineas recientes.

**Validaciones**:
- Servicio permitido si se informa.
- Cantidad de lineas positiva si se informa.

**Salida**:
- Logs recientes con encabezado de servicio.
- Mensaje en castellano si el servicio no existe o no esta en ejecucion.

## Status

**Entradas**:
- `Servicio`: opcional.

**Salida**:
- Estado de contenedor.
- Puertos esperados.
- Red esperada.
- Resultado de conectividad basica.
- Codigo de salida distinto de cero si algun servicio requerido esta detenido o degradado.
