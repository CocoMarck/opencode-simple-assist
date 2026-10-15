# Normalizador de TTS

Objetivo: convertir la respuesta markdown de Open Code en texto plano legible por
cualquier TTS (no atado a espeak). Funciones sueltas, solo stdlib (`re`).

**Archivo**: `tts/markdown.py` (reescribir el stub actual).

Sin truncado total. Sin dependencias nuevas. Sin cambios en `main.py`.

---

## Reglas, en este orden

El orden es crítico: el código y los enlaces van antes que las URLs, y las URLs
antes que las rutas.

1. Unificar saltos de línea (`\r\n`, `\r` -> `\n`).
2. Bloques de código ` ``` ``` ` y `~~~` -> `" caja de código "` (se descarta el
   contenido). Usar `re.DOTALL`.
3. Código en línea `` `x` `` -> se elimina. Evita el
   "comilla invertida, comilla invertida".
4. Enlaces `[texto](url)` -> se conserva solo `texto`.
5. URLs sueltas (`http://`, `https://`, `www.`) -> `" enlace "`.
6. Rutas de fichero (`~/...`, `/usr/...`, `./...`) -> se eliminan, con guarda
   `(?<![\w])` para **no comerse** `y/o` ni `1/2`.
7. Estructura markdown:
   - encabezados `#{1,6}`
   - viñetas `-`, `*`, `+`
   - listas numeradas `1.`
   - blockquote `>`
   - regla horizontal `---`
   - tablas `|`
8. Énfasis `**`, `__`, `*`, `_` -> se quitan.
9. Símbolos con voz propia:
   - `%` -> `" por ciento"`
   - `&` -> `" y "`
   - `+` -> `" mas "`
   - `@` -> `" arroba "`
10. Filtro final: dejar solo letras (acentos y `ñ` incluidas), dígitos, espacios
    y `. , ! ? ¿ ¡`. Esto arrastra emojis y elimina `#`, `>`, `<`.
11. Colapsar espacios (`\s+` -> un espacio) y `strip()`.
12. Descartar **tokens de más de 100 caracteres** (regla del `changelog.md`).
13. Descartar pensamientos, bloques de etiquetas, como: `<think></think>`.

---

## Decisiones tomadas

- Bloques de código -> frase `"caja de código"` (no se leen, pero se avisa).
- Código en línea -> se elimina.
- `#`, `>`, `<` -> se eliminan (no se leen); se sigue `idea.md`.
- `@` -> `" arroba"`.
- **Sin** límite de caracteres total (paso 7 de `idea.md` queda fuera por ahora).
- Palabras de más de 100 caracteres -> se descartan.
- Acentos y `ñ` se conservan; espeak-ng los pronuncia bien.

## Nota de divergencia entre docs

- `idea.md` dice *eliminar* bloques de código; `changelog.md` pedía *transcribirlos*
  a `"caja de código"`. Se eligió `"caja de código"`.
- `changelog.md` quería leer `@ # > <`; `idea.md` borra `# > <`. Se eligió `idea.md`.
- `changelog.md` pide descartar palabras >100 chars; `idea.md` solo habla del límite
  total. Se incluye el descarte por palabra.

---

## Tests

`tests/test_markdown.py` con `unittest` (stdlib). Un caso por regla más un caso
combinado:

- bloque -> `"caja de código"`, contenido fuera.
- código en línea eliminado.
- `[t](u)` -> `t`.
- URL -> `"enlace"`.
- rutas eliminadas, pero `y/o` y `1/2` intactos.
- `#` y viñetas fuera.
- `**` fuera.
- `% & + @` mapeados.
- `# < >` fuera.
- acentos, `ñ` y `. , ! ? ¿ ¡` conservados.
- token de más de 100 chars descartado.

Ejecutar:

```sh
python -m unittest discover -s tests -t .
```

Los paquetes `core/` y `tts/` funcionan como namespace packages (sin `__init__.py`).

---

## Fuera de alcance

- `run_text_to_speech` usa `os.system` con comillas (`main.py`); el filtro ya
  elimina comillas, así que no rompe, pero es candidato a `subprocess` después.
- Límite total de caracteres (`tts.maximo_caracteres`) pospuesto.
