# Contrato: Build de Imagenes

## Proposito

Define el comportamiento requerido para construir imagenes del stack completo o de un servicio
individual.

## Comando

```text
Scripts/BuildImages.sh [Servicio] [Version]
```

## Entradas

- `Servicio`: opcional. Si se omite, construye todas las imagenes.
- `Version`: opcional. Si se omite, usa la version declarada o `latest`.

## Validaciones

- El runtime Podman debe estar disponible.
- El servicio, si se informa, debe estar permitido.
- Cada Containerfile requerido debe existir antes de ejecutar builds.
- La version no puede estar vacia.

## Salidas Esperadas

- Mensajes en castellano por cada imagen construida.
- Resumen final con cantidad de imagenes construidas y fallidas.
- Codigo de salida cero si todo finaliza correctamente.
- Codigo de salida distinto de cero si falta una definicion o falla una construccion.

## Reglas

- El script no debe construir imagenes parciales si una definicion requerida falta en build total.
- Las etiquetas deben incluir proyecto, servicio y version.
- No debe agregar dependencias externas.
