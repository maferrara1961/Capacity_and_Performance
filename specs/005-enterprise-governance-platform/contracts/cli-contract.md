# Contrato CLI: Plataforma Enterprise de Gobierno

## Alcance

Este contrato define el comportamiento esperado de comandos para evaluacion enterprise, validacion,
sincronizacion de inventario y generacion de evidencia sintetica. Los nombres de comandos pueden
implementarse extendiendo scripts existentes o agregando nuevos scripts, pero el comportamiento debe
ser testeable desde shell.

## Reglas Comunes

- Los comandos deben validar todos los argumentos controlados por usuario antes de ejecutar.
- Los comandos deben imprimir mensajes operativos en castellano, consistentes con los scripts
  existentes.
- Los comandos deben retornar exit code `0` en exito y distinto de cero ante error de validacion o
  ejecucion.
- Los comandos destructivos deben requerir confirmacion explicita.
- Los comandos no deben requerir nuevas librerias externas.

## `Scripts/RunEnterpriseAssessment.sh`

Ejecuta scoring y evaluacion de riesgos enterprise para el alcance seleccionado.

### Argumentos Requeridos

- `--scope`: `enterprise`, `domain`, `service` o `component`.

### Argumentos Opcionales

- `--scope-id`: identificador requerido cuando scope no es `enterprise`.
- `--evidence-window-days`: entero positivo; default `90`.
- `--run-id`: run id provisto por caller; generado si se omite.

### Salida Exitosa

```text
INFO: evaluacion enterprise completada
  run: <AssessmentRunId>
  scope: <scope>
  scores: <count>
  risks: <count>
  recomendaciones: <count>
```

### Fallas de Validacion

- Scope desconocido.
- Falta `--scope-id` para scope no enterprise.
- Ventana de evidencia invalida.
- Contenedores requeridos faltantes o fuente de datos no disponible.

## `Scripts/ValidateEnterpriseGovernance.sh`

Valida que datasets y dashboards de gobierno enterprise sean utilizables.

### Argumentos Opcionales

- `--run-id`: validar un run especifico.
- `--scope`: validar un alcance especifico.

### Salida Exitosa

```text
INFO: validacion enterprise completada
  inventario: OK
  evidencia: OK
  scoring: OK
  riesgos: OK
  dashboards: OK
```

## `Scripts/GenerateEnterpriseVerificationData.sh`

Genera evidencia enterprise representativa para inventario, telemetria, ciclo de vida,
cumplimiento, confianza de monitoreo, riesgo, scoring y dashboards.

### Argumentos Opcionales

- `--profile`: `normal`, `warning`, `critical` o `mixed`.
- `--domains`: dominios tecnologicos separados por coma.
- `--services`: entero positivo.
- `--components`: entero positivo.
- `--days`: entero positivo, default `90`.
- `--load-id`: id de dataset provisto por caller.

### Modo Borrado

```bash
Scripts/GenerateEnterpriseVerificationData.sh delete --load-id <LoadId>
Scripts/GenerateEnterpriseVerificationData.sh delete --all --confirmar
```

El modo borrado debe eliminar solamente datos enterprise de verificacion generados.
