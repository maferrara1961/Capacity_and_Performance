# Quickstart: Scripts de Imagenes y Administracion

## Proposito

Validar que los scripts operativos construyen, inician, detienen, limpian, muestran logs e informan
estado del stack usando mensajes en castellano y respetando la interconexion entre servicios.

## Prerrequisitos

- Repositorio clonado.
- Podman disponible.
- Containerfiles existentes en `ContainerImages/`.
- Configuracion existente en `Config/PodmanStack.yml` y `Config/StackManifest.yml`.

## 1. Validar comandos y configuracion

```bash
Scripts/ValidateStack.sh
```

Resultado esperado:
- Se informa que la configuracion base es valida.
- No se informan dependencias externas nuevas.

## 2. Construir todas las imagenes

```bash
Scripts/BuildImages.sh
```

Resultado esperado:
- Se validan todos los Containerfiles antes de construir.
- Se construyen las imagenes requeridas.
- Se muestra resumen en castellano.

## 3. Construir una imagen individual

```bash
Scripts/BuildImages.sh Grafana v1.0.0
```

Resultado esperado:
- Solo se construye la imagen de Grafana.
- La etiqueta incluye proyecto, servicio y version.

## 4. Iniciar el stack

```bash
Scripts/StartStack.sh
```

Resultado esperado:
- Se crea o reutiliza la red comun.
- Los servicios se inician en orden compatible con dependencias.
- El script informa estado saludable o detalle del servicio fallido.

## 5. Consultar estado

```bash
Scripts/StackStatus.sh
Scripts/StackStatus.sh Grafana
```

Resultado esperado:
- Se muestran contenedores, puertos, red y salud basica.
- Si un servicio esta detenido, el resultado lo informa en castellano.

## 6. Consultar logs

```bash
Scripts/StackLogs.sh Grafana 100
```

Resultado esperado:
- Se muestran las ultimas 100 lineas del servicio Grafana.
- Si el servicio no existe, se devuelve error determinista en castellano.

## 7. Detener el stack

```bash
Scripts/StopStack.sh
```

Resultado esperado:
- Los contenedores administrados se detienen.
- Los volumenes persistentes permanecen.

## 8. Limpieza explicita

```bash
Scripts/CleanupStack.sh --confirmar
```

Resultado esperado:
- Solo se eliminan recursos temporales permitidos.
- No se eliminan volumenes persistentes por defecto.
