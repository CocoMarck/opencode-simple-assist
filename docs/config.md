# Simple Assist Config
Un archivo simple, para configurar el asistente, y sus dependencias. Este archivo siempre debe existir, si no existe, pues no jala el programa.

Deberá existir en el `workdir/config/archivo.toml`, de este programa, y en `workdir/archivo.toml` del open code.

Se podría generar un config default, pero bueno, capaz sea bueno solo detectar que no existe, y pasar a exception.

## Datos
- `model`, string de modelo a usar. Tiene que existir en `opencode models`. Responsabilidad de `OpenCodeManager class`, el saber si existe el modelo.
- `name`, string de nombre del asistente. El `AGENTS.md`, apuntara a que su nombre esta en el `file.toml` de su directorio de trabajo. (Así se evita escribir a cada rato `AGENTS.md`). Para `SimpleAssist class`.
- `memory_in_days`, int de días en los que mantiene en uso una misma sesión. Para `SimpleAssist class`.
- `response_timeout_in_seconds`, int segundos de espera de respuesta. Para `OpenCodeManager class`.