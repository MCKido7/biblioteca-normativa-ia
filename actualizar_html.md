# Actualizar biblioteca.html

`biblioteca.html` es una página de un solo archivo: lleva dentro los datos de `biblioteca.xlsx` y el texto de todas las fichas. No se actualiza sola. Hay que regenerarla cuando cambie la biblioteca (documentos nuevos, cambios de estado, fichas editadas).

## Cómo se genera

- `herramientas/biblioteca_plantilla.html`: el diseño y el código de la página (sin datos).
- `herramientas/construir_biblioteca_html.py`: lee `biblioteca.xlsx` y `/fichas`, los mete en la plantilla y escribe `biblioteca.html`.
- `herramientas/cambios_estado.json` (opcional): lista de cambios de estado para el apartado «Novedades». Formato: `[{"id": "C03", "de": "PENDIENTE", "a": "recurrido / anulado", "fecha": "2026-11-26"}]`.

Para regenerar a mano, desde la carpeta de la biblioteca (necesita `openpyxl`):

```powershell
python herramientas/construir_biblioteca_html.py
```

## Prompt para pedírselo al agente

```
Regenera biblioteca.html con los datos actuales.

1. Comprueba que biblioteca.xlsx y /fichas coinciden: cada fila del Excel tiene su ficha y su archivo en /normas, /guias o /casos. Si algo no coincide, dímelo y no sigas.
2. Si desde la última versión ha cambiado el estado de algún documento, añade esa entrada a herramientas/cambios_estado.json (id, estado anterior, estado nuevo, fecha). Sácalo del informe más reciente de /novedades o de lo que te diga yo; no inventes cambios.
3. Ejecuta python herramientas/construir_biblioteca_html.py y comprueba que no da avisos.
4. Abre biblioteca.html y comprueba: que la fecha de última actualización es la de hoy, que el número de documentos es el de biblioteca.xlsx, que los filtros y el buscador funcionan, que la ficha completa se abre y que «Exportar a CSV» descarga solo lo filtrado.
5. Si el cuadro «Pregunta a la biblioteca» responde con algo que no está en las fichas, o sin citar el ID, es un error: corrígelo en la plantilla.
6. Dime cuántos documentos hay, cuántos son nuevos desde la versión anterior y qué has comprobado.

Límites: no edites biblioteca.xlsx ni las fichas; no descargues nada; la página no debe cargar nada de internet (sin CDN, fuentes ni scripts externos).
```

## Qué hace la página (para comprobar a mano)

1. **Novedades:** documentos con `fecha_alta` de las últimas cuatro semanas y cambios de estado de `cambios_estado.json`. Sin histórico previo, el primer día salen todos como nuevos.
2. **Pregunta a la biblioteca:** busca palabras en las fichas y muestra frases literales con el ID. No genera texto ni usa internet. Si no hay coincidencias, dice «No consta en las fichas».
3. **Buscador y filtros:** tipo, ámbito, tema, estado y vinculante.
4. **Línea de tiempo:** las fechas de «Fechas clave» de las fichas visibles. Solo salen las que empiezan por AAAA-MM o AAAA-MM-DD.
5. **Exportar a CSV:** exporta lo que se ve con los filtros, con `;` como separador y codificación UTF-8 con BOM para abrirlo bien en Excel.

## Antes de proyectar

- Mira la fecha de «Última actualización» de la cabecera.
- Haz las tres comprobaciones de `rubrica.md`: abre dos fichas, busca «decisiones automatizadas» y revisa los estados de N04 y C03.
