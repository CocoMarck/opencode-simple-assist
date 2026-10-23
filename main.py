import os, sys, random
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

# Módulos Simple Assist
from core.open_code_manager import OpenCodeManager
from core.espeak_manager import EspeakManager
from core.simple_voice_assist import SimpleVoiceAssist
from core.simple_assist import SimpleAssist
from core.workdir_manager import WorkdirManager
from core.agent_manager import AgentManager
from tts import markdown

# Views QT
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow

# Init Assist Paths
data_home = os.environ.get("XDG_DATA_HOME")
home_dir = None
if data_home:
    home_dir = Path(data_home).joinpath(".local", "share")
else:
    home_dir = Path.home().joinpath(".local", "share")
workdir = home_dir.joinpath("simple_assist")

base = Path().parent.absolute()
TEMPLATES_DIR = base.joinpath("templates")
print(workdir)
print(TEMPLATES_DIR)

SIMPLE_ASSIST_FILE = base.joinpath("config", "simple_assist.toml")

MAIN_WINDOW_UI_FILE = base.joinpath("views", "main_window.ui")

# Templates
environment = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


# Init config
import tomllib
with open(SIMPLE_ASSIST_FILE, "rb") as f:
    data = tomllib.load(f)
print(data)


# Palabra clave, para recibir ordenes.
keyword = data["name"]
timeout = data["response_timeout_in_seconds"]

# Inicializar módulos
agent_manager = AgentManager(name=keyword, environment=environment)
workdir_manager = WorkdirManager(workdir, agent_manager, SIMPLE_ASSIST_FILE)
workdir_manager.ensure()
open_code_manager = OpenCodeManager(timeout=timeout, workdir=workdir)
espeak_manager = EspeakManager()
simple_voice_assist = SimpleVoiceAssist(
    keyword, open_code_manager, espeak_manager, 
    data["memory_in_days"], data["model"])
simple_assist = SimpleAssist(
    open_code_manager=open_code_manager, espeak_manager=espeak_manager, 
    memory_in_days=data["memory_in_days"], model=data["model"])

# Construcción de prompt con `Speech to Text`
text = random.choice([
    "Dime una frase aleatoria por favor.",
    "Dime un dato curioso sobre los seres vivos.",
    "Dime un dato curioso sobre los mecanismos de la tecnología humana.",
    "Haz un poco de freestyle. No la hagas adentro de una caja de código.",
    f"Dime para que sirve un {keyword}.",
    "Abre el navegador predeterminado porfavor. Ya sea una nueva pestaña si es que ya existe un proceso, o un proceso nuevo si es que no hay.",
    "Escribe unas tres lineas de código python. De lo que sea, y escribe su resultado. (Escribe en el chat, no escribas archivos) (Puedes usar tu sandbox para probar).",
    "Describe resolución de problema matemático, muy sencillo pero con símbolos matemáticos raros.",
    "Abre la aplicación calculadora.",
    "Reproduce algo de música, con la aplicación multimedia que prefieras.",
    "Hola, porfavor, simplemente escribe un poco de texto. Es por fines debug.",
])

# Debug normalize text
markdown_text = (
f'''
# Texto Markdown para debug.

<think>Pensando mucho</think>
```python
palabras = ['hola', 'mundo', 'python']
print(' '.join(sorted(palabras, key=len)))
```

Salida: `hola mundo python`

</think>Ya no quiero pensar.

Que cosas.

```planote
Mas código para trolear al normalizer.
```

PalabraFalsaDemasiadaLargaParaSerLeidaPorqueEsParaTrolearAlTTSPorqueElTTSTieneLimitesAsíComoLosHumanosJajaSaludosCreoQueYaSonMasDeCienCaracteres

Una pregunta realista ¿El porque del todo, es algo que importa?, ¿O la pregunta es la que importa?.

Esto que sigue de los dos puntos, no se debe leer: {"@$#*"*10}.

Ahora modo bilingüe: 
    - 这是中文.
    - Это русский язык.
    - זה רוסי.
    - Kjo është shqipe.
    - और मैं पहले से ही थक गया हूँ, लेकिन आखिरी उपाय के तौर पर, इंडियन, टेस्टी करी।.

Ahora un problema matemático con símbolos raros: x ≔ 15 ⊘ 3 = 5.

La verdad no se como implementar: "∈, "□", "∎", "≔", "ℝ", "⊹". Así que solo los mencionare a lo loco, a espera ya lo hice.

Ahora muchas letras para ver si limita cantidad de palabras: {"a e i o u "*500}.
''' )
if True:
    print("Raw text:", markdown_text)
    if False:
        espeak_manager.speak(markdown.normalize( markdown_text))
    else:
        print("Normalized text:", markdown.normalize( markdown_text) )
    
else:
    simple_voice_assist.request_by_keyword( f"{keyword}. {text}" )
    #simple_assist.request(text)

# Views app
def main():
    app = QApplication( sys.argv )
    main_window = MainWindow(MAIN_WINDOW_UI_FILE, simple_assist)
    main_window.show()
    sys.exit( app.exec() )
if __name__ == '__main__':
    main()