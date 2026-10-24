# Instalación de Vosk para Python en Debian 13 (sin romper el sistema)

El objetivo es instalar [Vosk](https://alphacephei.com/vosk/) para usarlo con Python en Debian 13, sin usar `pip` a nivel global ni `--break-system-packages`. 

> Nota: Este proyecto ya menciona usar `uv` como gestor de paquetes, por lo que ambas opciones (venv + pip y uv) están cubiertas.

## 1 Dependencias del sistema

Vosk necesita algunas librerías para funcionar correctamente (sobre todo si vas a capturar audio con el micrófono). Instala estas con `apt`:

```bash
sudo apt update
sudo apt install -y \
  python3-venv \
  python3-pip \
  portaudio19-dev \
  libportaudio2 \
  pulseaudio-utils \
  alsa-utils \
  unzip \
  wget
```

## 2 Crear un entorno virtual

Nunca instales vosk directamente con pip en el sistema. Usa un entorno virtual aislado.

#### Opción A: `venv` (estándar, viene con Python)
```bash
mkdir -p ~/Proyectos/mi-asistente
cd ~/Proyectos/mi-asistente

# Crear entorno virtual
python3 -m venv .venv

# Activarlo
source .venv/bin/activate

# Actualizar pip dentro del entorno
pip install --upgrade pip
```

#### Opción B: uv (recomendado si ya lo usas en este repo)
[uv](https://docs.astral.sh/uv/) gestiona entornos y dependencias muy rápido. Puedes instalarlo con `pipx` para no tocar el sistema:
```bash
sudo apt install -y pipx
pipx ensurepath
# Cierra y vuelve a abrir la terminal, o recarga tu shell

cd ~/Proyectos/mi-asistente

# Crear entorno virtual
uv venv

# Activarlo
source .venv/bin/activate
```

## 3 Instalar Vosk

Con el entorno virtual activado:
Si usas `venv + pip`: 
```bash
pip install vosk
```

Si usas uv
```bash
uv pip install vosk
```

En Debian 13 (Python 3.13) los wheels oficiales de Vosk suelen estar disponibles. Si por alguna razón no hay wheel para tu arquitectura, necesitarás compilar dependencias, pero es poco común.

## 4 Descargar un modelo de Vosk
Los modelos no se instalan con `pip`, se descargan por separado. Para español el proyecto hace referencia a `vosk-model-small-es-0.42`.

```bash
# Desde la raíz de tu proyecto
mkdir -p models
cd models

# Descargar modelo pequeño para español
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip

# Descomprimir
unzip vosk-model-small-es-0.42.zip

# Limpiar zip
rm vosk-model-small-es-0.42.zip

# Volver a la raíz
cd ..
```

La ruta quedará así: `models/vosk-model-small-es-0.42/`

Puedes ver más modelos en [alphacephei.com/vosk/models](https://alphacephei.com/vosk/models). Para uso con CPU y en tiempo real, small es más que suficiente.

## 5 Prueba rápida
Crea un archivo `test_vosk.py` para verificar la instalación:
```python
from vosk import Model, KaldiRecognizer
import json

# Cargar modelo
model = Model("models/vosk-model-small-es-0.42")
rec = KaldiRecognizer(model, 16000)

# Ejemplo: probar con un archivo wav de 16kHz mono si lo tienes
# o usarlo con tu micrófono con pyaudio/parec según tu implementación
print("Modelo cargado correctamente")
```

Ejecuta con el entorno activado: `python test_vosk.py`

Si no hay errores, Vosk está correctamente instalado. Trucos y recomendaciones para no romper el sistema:
- Siempre `virtualenv`: activa `.venv` antes de instalar o ejecutar código.
- Sin `--break-system-packages`: si te lo sugiere pip, significa que estás fuera del entorno virtual. Detente y actívalo.
- Usa `pipx` para herramientas CLI: si necesitas instalar alguna herramienta global, usa `pipx` en lugar de pip.
- Modelos fuera del sitio de paquetes: guarda los modelos en tu proyecto/directorio de datos (como hace este proyecto con `~/.local/share/simple-assist`).
- Audio en `Debian/Wayland/PipeWire`: si vas a usar micrófono, `parec/pw-record` funcionan bien. Asegúrate de tener permisos para tu tarjeta de audio (usualmente con el usuario en el grupo audio o pulse).
- Limpieza: para desinstalar, basta con borrar el directorio `.venv/` y los modelos. No quedan rastros en el sistema.