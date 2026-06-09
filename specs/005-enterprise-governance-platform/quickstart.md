# Quickstart: Plataforma Enterprise de Gobierno

## Prerrequisitos

- Podman disponible en el host.
- Repositorio clonado y en `main`.
- Imagenes del stack construidas.
- Sin nuevos paquetes externos de Python instalados.

## 1. Validar el Repositorio

```bash
Scripts/ValidateStack.sh
Scripts/RunTests.sh
```

Resultado esperado:

```text
Validacion del stack completada correctamente
OK
```

## 2. Iniciar el Stack

```bash
Scripts/BuildImages.sh
Scripts/StartStack.sh
Scripts/StackStatus.sh
```

Resultado esperado:

- PostgreSQL saludable.
- VictoriaMetrics saludable.
- ZabbixServer saludable.
- ZabbixWeb saludable.
- Grafana saludable.
- CapacityEngine completado correctamente o listo para ejecucion batch.

## 3. Generar Evidencia Enterprise de Verificacion

Comando de validacion planificado:

```bash
Scripts/GenerateEnterpriseVerificationData.sh --profile mixed --domains all --services 5 --components 50 --days 90 --load-id EnterpriseDemo001
```

Resultado esperado:

- Existen registros de inventario para multiples dominios tecnologicos.
- Los servicios de negocio mapean a componentes tecnologicos.
- Los registros de evidencia incluyen estados disponible, faltante, desconocido, incompleto y no
  verificado.
- Existen evaluaciones de score en rango 0-100.
- Los registros de riesgo identifican tecnologias y servicios afectados.
- Las recomendaciones estan vinculadas a riesgos y evidencia.

## 4. Ejecutar Evaluacion Enterprise

Comando de validacion planificado:

```bash
Scripts/RunEnterpriseAssessment.sh --scope enterprise --evidence-window-days 90 --run-id EnterpriseRun001
```

Resultado esperado:

```text
INFO: evaluacion enterprise completada
  run: EnterpriseRun001
  scope: enterprise
  scores: <count>
  risks: <count>
  recomendaciones: <count>
```

## 5. Validar Salidas de Gobierno

Comando de validacion planificado:

```bash
Scripts/ValidateEnterpriseGovernance.sh --run-id EnterpriseRun001
```

Resultado esperado:

```text
INFO: validacion enterprise completada
  inventario: OK
  evidencia: OK
  scoring: OK
  riesgos: OK
  dashboards: OK
```

## 6. Revisar Dashboards

Abrir Grafana:

```text
http://localhost:3000
```

Comportamiento esperado de dashboards:

- El dashboard ejecutivo muestra Technology Health Score y scores por dominio.
- El mapa de calor de riesgo muestra riesgo por dominio tecnologico.
- Top riesgos incluye tecnologias afectadas, servicios afectados, severidad, impacto y accion
  recomendada.
- La evidencia faltante o incompleta es visible y no se trata como saludable.
- Los dashboards operativos muestran tendencias, horizontes de forecast, top consumidores y
  frescura de evidencia.

## 7. Limpiar Datos de Verificacion

Comando de validacion planificado:

```bash
Scripts/GenerateEnterpriseVerificationData.sh delete --load-id EnterpriseDemo001
```

Resultado esperado:

- Los registros generados de verificacion se eliminan.
- El inventario operativo no generado y la evidencia administrada manualmente permanecen intactos.

## Referencias

- [Modelo de datos](./data-model.md)
- [Contrato CLI](./contracts/cli-contract.md)
- [Contrato de dashboards](./contracts/dashboard-contract.md)
- [Contrato de dataset](./contracts/dataset-contract.md)
