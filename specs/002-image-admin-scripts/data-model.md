# Modelo de Datos: Scripts de Imagenes y Administracion

## Entidad: ServicioDelStack

**Proposito**: Representa un componente administrado por los scripts.

**Campos**:
- `Nombre`: Nombre permitido del servicio.
- `Imagen`: Nombre completo de imagen esperada.
- `Contenedor`: Nombre del contenedor administrado.
- `Containerfile`: Ruta de definicion de imagen.
- `Puertos`: Lista de puertos publicados.
- `Dependencias`: Servicios que deben estar disponibles antes de iniciar.
- `Volumenes`: Volumenes persistentes asociados.
- `VariablesRequeridas`: Variables necesarias para el arranque.

**Relaciones**:
- Tiene una `ImagenDelServicio`.
- Puede depender de otros `ServicioDelStack`.
- Puede usar uno o mas `VolumenPersistente`.
- Pertenece a una `RedDelStack`.

**Reglas de Validacion**:
- `Nombre`, `Imagen`, `Contenedor` y `Containerfile` son obligatorios.
- `Nombre` debe estar en la lista permitida.
- Las dependencias deben referenciar servicios existentes.
- Los puertos no pueden repetirse dentro del stack.

## Entidad: ImagenDelServicio

**Proposito**: Define una imagen construible del stack.

**Campos**:
- `Servicio`: Servicio asociado.
- `Etiqueta`: Tag completo de imagen.
- `Version`: Version aplicada.
- `RutaContainerfile`: Ruta esperada.
- `EstadoConstruccion`: Pendiente, Construida, Fallida.

**Relaciones**:
- Pertenece a `ServicioDelStack`.

**Reglas de Validacion**:
- La ruta del Containerfile debe existir antes de construir.
- La version no puede estar vacia.
- La etiqueta debe incluir proyecto, servicio y version.

## Entidad: RedDelStack

**Proposito**: Representa la red compartida para interconexion.

**Campos**:
- `Nombre`: Nombre de red.
- `ServiciosConectados`: Servicios esperados en la red.
- `Estado`: Ausente, Creada, Incompatible.

**Relaciones**:
- Contiene multiples `ServicioDelStack`.

**Reglas de Validacion**:
- Si la red existe, debe ser compatible con el stack.
- La red se crea antes de iniciar servicios.

## Entidad: VolumenPersistente

**Proposito**: Recurso de datos que debe sobrevivir a stop.

**Campos**:
- `Nombre`: Nombre del volumen.
- `ServicioPropietario`: Servicio que lo usa.
- `PoliticaLimpieza`: Preservar, Temporal, LimpiezaExplicita.

**Relaciones**:
- Pertenece a uno o mas `ServicioDelStack`.

**Reglas de Validacion**:
- Stop nunca elimina volumenes con politica Preservar.
- Cleanup solo elimina recursos permitidos por politica.

## Entidad: ComandoOperativo

**Proposito**: Accion solicitada por el operador.

**Campos**:
- `Accion`: Build, Start, Stop, Logs, Status, Cleanup.
- `Servicio`: Servicio opcional.
- `Version`: Version opcional.
- `CantidadLineas`: Cantidad opcional para logs.
- `ConfirmacionDestructiva`: Indicador para acciones destructivas.

**Relaciones**:
- Puede aplicar a un `ServicioDelStack`.

**Reglas de Validacion**:
- La accion debe estar permitida.
- Si se informa servicio, debe existir en la lista permitida.
- `CantidadLineas` debe ser positiva.
- Acciones destructivas requieren confirmacion explicita.

## Entidad: ResultadoDeSalud

**Proposito**: Resultado de una validacion operativa.

**Campos**:
- `Servicio`: Servicio evaluado.
- `Estado`: Saludable, Degradado, Detenido, Desconocido.
- `PuertoDisponible`: Indicador de puerto.
- `RedDisponible`: Indicador de red.
- `Mensaje`: Mensaje en castellano.

**Relaciones**:
- Se genera desde `ComandoOperativo` Status o Start.

**Reglas de Validacion**:
- Todo resultado debe incluir mensaje.
- Estados no saludables deben retornar codigo de salida distinto de cero.

## Transiciones de Estado

### ServicioDelStack

```text
Ausente -> ImagenConstruida -> ContenedorCreado -> EnEjecucion
EnEjecucion -> Detenido
Detenido -> EnEjecucion
EnEjecucion -> Fallido
Fallido -> Detenido
```

### ImagenDelServicio

```text
Pendiente -> Construida
Pendiente -> Fallida
Fallida -> Pendiente
```
