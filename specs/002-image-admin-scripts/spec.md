# Especificacion de Feature: Scripts de Imagenes y Administracion

**Rama de Feature**: `002-image-admin-scripts`

**Creado**: 2026-06-08

**Estado**: Borrador

**Entrada**: Descripcion del usuario: "Crear en nueva rama, los script de creacion de imagenes y administracion, build, start, stop, logs - Teniendoe en cuenta la interconexion de las ditintas imagenes -- Escribir todo en castellano"

## Escenarios de Usuario y Pruebas *(obligatorio)*

### Historia de Usuario 1 - Construir imagenes del stack (Prioridad: P1)

Como operador de plataforma, necesito ejecutar un unico flujo de construccion para crear las
imagenes del stack de capacidad y rendimiento, de modo que todas las imagenes queden versionadas,
nombradas y listas para ejecutarse juntas.

**Por que esta prioridad**: Sin imagenes construidas de forma repetible no se puede administrar el
ciclo de vida del stack ni validar la interconexion entre componentes.

**Prueba Independiente**: Ejecutar el script de build en un entorno limpio y verificar que se
construyen las imagenes requeridas, que cada imagen tiene nombre y version esperados, y que el
script falla con un mensaje claro si falta un Containerfile.

**Escenarios de Aceptacion**:

1. **Dado** que todos los Containerfiles existen, **cuando** el operador ejecuta el script de build, **entonces** se construyen todas las imagenes necesarias y se informa un resumen exitoso.
2. **Dado** que falta una definicion de imagen requerida, **cuando** el operador ejecuta el script de build, **entonces** el proceso se detiene antes de construir parcialmente el stack y muestra que archivo falta.

---

### Historia de Usuario 2 - Iniciar servicios interconectados (Prioridad: P2)

Como operador de plataforma, necesito iniciar los contenedores en el orden correcto y con la red,
variables, puertos y dependencias necesarias para que los componentes se comuniquen entre si.

**Por que esta prioridad**: El valor del stack depende de que PostgreSQL, VictoriaMetrics, Zabbix,
Grafana y el motor de capacidad puedan resolverse y comunicarse correctamente.

**Prueba Independiente**: Ejecutar el script de start y verificar que se crea la red comun, que se
inician los servicios en orden de dependencia, y que cada servicio expone los puertos esperados.

**Escenarios de Aceptacion**:

1. **Dado** que las imagenes ya existen, **cuando** el operador ejecuta start, **entonces** se crea o reutiliza la red del stack y los servicios quedan en ejecucion.
2. **Dado** que un servicio dependiente no esta disponible, **cuando** el operador ejecuta start, **entonces** el script informa la dependencia fallida y evita reportar el stack como saludable.

---

### Historia de Usuario 3 - Detener y limpiar servicios de forma segura (Prioridad: P3)

Como operador de plataforma, necesito detener el stack sin perder datos persistentes y con una
opcion explicita para limpieza controlada, de modo que pueda reiniciar o mantener el entorno sin
acciones manuales riesgosas.

**Por que esta prioridad**: La administracion segura evita perdida accidental de datos y deja el
entorno en un estado conocido.

**Prueba Independiente**: Ejecutar stop y verificar que los contenedores se detienen sin borrar
volumenes persistentes; ejecutar una limpieza explicita y verificar que solo elimina recursos
temporales permitidos.

**Escenarios de Aceptacion**:

1. **Dado** que el stack esta en ejecucion, **cuando** el operador ejecuta stop, **entonces** todos los contenedores administrados se detienen y los datos persistentes permanecen.
2. **Dado** que el operador solicita limpieza explicita, **cuando** ejecuta el comando correspondiente, **entonces** se eliminan solo redes o contenedores temporales definidos por el stack.

---

### Historia de Usuario 4 - Consultar logs y estado operativo (Prioridad: P4)

Como operador de plataforma, necesito consultar logs y estado de cada componente o del stack
completo para diagnosticar fallas de construccion, arranque, conectividad o ejecucion.

**Por que esta prioridad**: La operacion diaria requiere visibilidad rapida de errores sin conocer
comandos internos ni nombres exactos de contenedores.

**Prueba Independiente**: Ejecutar logs y status con filtros por servicio y validar que se muestran
mensajes recientes, estado de contenedor, puertos y resultado de chequeos basicos de conectividad.

**Escenarios de Aceptacion**:

1. **Dado** que el stack esta en ejecucion, **cuando** el operador solicita logs de Grafana, **entonces** ve los logs recientes del contenedor correcto.
2. **Dado** que un servicio esta detenido, **cuando** el operador consulta status, **entonces** el servicio aparece como detenido y el script retorna estado no saludable.

### Casos Borde

- El runtime de contenedores no esta instalado o no esta disponible para el usuario actual.
- Una imagen requerida no existe antes de iniciar el stack.
- Ya existe un contenedor con el mismo nombre.
- Ya existe una red con el mismo nombre pero configuracion incompatible.
- Un puerto requerido ya esta ocupado.
- Una variable de entorno requerida falta o esta vacia.
- Un servicio inicia pero no responde dentro del tiempo esperado.
- El operador pide logs de un servicio inexistente.
- El script se ejecuta desde un directorio distinto a la raiz del repositorio.

## Requisitos *(obligatorio)*

### Requisitos Funcionales

- **RF-001**: El sistema DEBE proveer un script de build que construya todas las imagenes requeridas del stack.
- **RF-002**: El sistema DEBE permitir construir una imagen individual sin reconstruir todas las demas.
- **RF-003**: El sistema DEBE etiquetar las imagenes con nombre de proyecto, nombre de servicio y version.
- **RF-004**: El sistema DEBE validar que cada definicion de imagen requerida exista antes de iniciar la construccion.
- **RF-005**: El sistema DEBE proveer un script de start que cree o reutilice una red comun del stack.
- **RF-006**: El sistema DEBE iniciar los servicios en orden compatible con sus dependencias.
- **RF-007**: El sistema DEBE configurar nombres de contenedores, puertos, volumenes y variables necesarias para la interconexion.
- **RF-008**: El sistema DEBE verificar conectividad basica entre componentes despues del arranque.
- **RF-009**: El sistema DEBE proveer un script de stop que detenga los contenedores administrados sin borrar datos persistentes.
- **RF-010**: El sistema DEBE proveer una accion de limpieza explicita para recursos temporales del stack.
- **RF-011**: El sistema DEBE proveer un script de logs que permita consultar logs del stack completo o de un servicio especifico.
- **RF-012**: El sistema DEBE proveer un script de status que informe estado, puertos, red y salud basica de los servicios.
- **RF-013**: El sistema DEBE mostrar mensajes de error en castellano para entradas invalidas, dependencias faltantes y fallas operativas.
- **RF-014**: El sistema DEBE validar todas las entradas controladas por el usuario antes de ejecutar acciones sobre contenedores.
- **RF-015**: El sistema DEBE rechazar nombres de servicio no permitidos en acciones como build individual, logs o status.
- **RF-016**: El sistema DEBE funcionar sin agregar librerias externas, SDKs, paquetes o servicios alojados nuevos.
- **RF-017**: Los simbolos y artefactos definidos por el proyecto DEBEN usar PascalCase salvo convenciones obligatorias de plataforma documentadas.

### Entidades Clave *(incluido si la feature involucra datos)*

- **ServicioDelStack**: Componente administrado del stack; incluye nombre, imagen, contenedor, puertos, dependencias, volumenes y estado esperado.
- **ImagenDelServicio**: Imagen construible asociada a un servicio; incluye ruta de definicion, etiqueta, version y estado de construccion.
- **RedDelStack**: Red compartida por los contenedores; incluye nombre, servicios conectados y validaciones de resolucion.
- **VolumenPersistente**: Recurso de datos que debe sobrevivir a stop; incluye nombre, servicio propietario y politica de limpieza.
- **ComandoOperativo**: Accion solicitada por el operador; incluye build, start, stop, logs, status y cleanup.
- **ResultadoDeSalud**: Resultado de validacion operativa; incluye servicio, estado, puertos, conectividad y mensaje.

## Criterios de Exito *(obligatorio)*

### Resultados Medibles

- **CE-001**: Un operador puede construir todas las imagenes del stack con un solo comando y recibir un resumen final en menos de 2 minutos en un entorno con cache local.
- **CE-002**: El script de start deja el 100% de los servicios requeridos en estado en ejecucion o informa explicitamente cual fallo.
- **CE-003**: El script de status detecta servicios detenidos, puertos no disponibles o red faltante en menos de 30 segundos.
- **CE-004**: El script de logs permite consultar logs de cualquier servicio permitido con un solo comando.
- **CE-005**: Stop preserva el 100% de los volumenes persistentes salvo que el operador solicite limpieza explicita.
- **CE-006**: El 100% de las entradas invalidas cubiertas por pruebas devuelve errores deterministas en castellano.
- **CE-007**: Los scripts pueden ejecutarse desde cualquier directorio dentro del repositorio y resolver correctamente la raiz del proyecto.

## Alineacion con la Constitucion *(obligatorio)*

- **Testeabilidad**: Cada comando operativo tiene escenarios verificables para entradas validas, entradas invalidas, dependencias faltantes e interconexion.
- **Clean Architecture**: Las reglas de servicios, dependencias, validacion y nombres permitidos se mantienen separadas de la ejecucion concreta del runtime de contenedores.
- **Validacion**: Las entradas controladas por el usuario incluyen nombre de servicio, accion solicitada, version, rutas, flags de limpieza y cantidad de logs.
- **Acceso Protegido**: Los scripts operan sobre recursos locales del stack; no agregan rutas protegidas nuevas. Las credenciales usadas por servicios se consumen desde configuracion validada y no se imprimen en logs.
- **Restriccion de Dependencias**: La feature no agrega librerias externas ni servicios alojados; usa las herramientas ya aprobadas del stack y capacidades del sistema.
- **Nombres**: Los archivos y simbolos propios usan PascalCase cuando la plataforma lo permite; nombres de contenedores, flags y comandos pueden usar convenciones de shell documentadas.

## Supuestos

- El runtime principal sera Podman, coherente con la implementacion existente del stack.
- Los scripts se ejecutaran en sistemas tipo Linux o macOS con shell compatible.
- La limpieza destructiva de volumenes persistentes queda fuera del comportamiento por defecto.
- Los nombres de servicios permitidos son los componentes ya definidos en el stack: Zabbix, VictoriaMetrics, Grafana, PostgreSQL y CapacityEngine.
- Toda salida destinada al operador debe estar en castellano.
- Los comandos deben poder ejecutarse desde la raiz del repositorio o desde subdirectorios.
