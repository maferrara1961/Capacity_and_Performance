# Investigacion: Scripts de Imagenes y Administracion

## Decision: Usar scripts shell con archivo comun de reglas

**Razon**: El proyecto ya usa scripts shell para operar el stack. Un archivo comun permite mantener
una unica lista de servicios, imagenes, contenedores, puertos, volumenes y dependencias sin agregar
dependencias externas.

**Alternativas consideradas**:
- Reescribir la administracion en Python: rechazado porque los comandos son operaciones directas de
  sistema y shell reduce complejidad.
- Usar una herramienta externa de orquestacion: rechazado por la restriccion de no agregar
  dependencias.
- Duplicar reglas en cada script: rechazado por DRY.

## Decision: Podman es el runtime operativo

**Razon**: La feature anterior y la especificacion del stack ya usan Podman. Mantener Podman evita
dos caminos operativos y respeta la arquitectura existente.

**Alternativas consideradas**:
- Soportar Docker en paralelo: rechazado para la primera version por YAGNI.
- Detectar multiples runtimes automaticamente: rechazado porque complica pruebas y mensajes.

## Decision: `Config/StackManifest.yml` y `Config/PodmanStack.yml` siguen siendo fuentes de verdad

**Razon**: Ya existen artefactos de configuracion con componentes aprobados y definicion del stack.
Los scripts deben validarlos y consumirlos, no crear una fuente paralela.

**Alternativas consideradas**:
- Guardar metadata en cada script: rechazado por duplicacion.
- Generar configuracion dinamica sin archivo declarativo: rechazado porque dificulta auditoria.

## Decision: Salida de operador completamente en castellano

**Razon**: El usuario lo pidio explicitamente. Los mensajes operativos, errores y resumenes deben
ser comprensibles para operadores hispanohablantes.

**Alternativas consideradas**:
- Mensajes bilingues: rechazado para evitar ruido.
- Mantener mensajes tecnicos en ingles: rechazado salvo identificadores de servicios, comandos o
  flags.

## Decision: Stop conserva volumenes por defecto y cleanup es explicito

**Razon**: La feature debe evitar perdida accidental de datos. Stop solo detiene contenedores;
cleanup borra recursos temporales definidos y cualquier accion destructiva debe ser explicita.

**Alternativas consideradas**:
- Stop con limpieza automatica: rechazado por riesgo operativo.
- Cleanup de volumenes por defecto: rechazado por riesgo de perdida de datos.

## Decision: Pruebas sin contenedores reales para contratos basicos

**Razon**: Los contratos de validacion, parsing, nombres permitidos y mensajes pueden probarse sin
levantar contenedores. Las pruebas de runtime real quedan como smoke tests manuales o de entorno.

**Alternativas consideradas**:
- Requerir Podman real en todas las pruebas: rechazado porque dificulta ejecucion local y CI.
- No probar scripts shell: rechazado por TDD y criticidad operativa.
