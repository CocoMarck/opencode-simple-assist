import random

# Módulos
from core.open_code_manager import OpenCodeManager
from core.espeak_manager import EspeakManager
from core.simple_voice_assist import SimpleVoiceAssist
from core.simple_assist import SimpleAssist
from tts import markdown

# Palabra clave, para recibir ordenes.
keyword = "Asistente"

# Inicializar módulos
open_code_manager = OpenCodeManager(timeout=60)
espeak_manager = EspeakManager()
simple_voice_assist = SimpleVoiceAssist(keyword, open_code_manager, espeak_manager)
simple_assist = SimpleAssist(open_code_manager, espeak_manager)

# Construcción de prompt con `Speech to Text`
text = random.choice([
    "Dime una frase aleatoria por favor.",
    "Dime un dato curioso sobre los seres vivos.",
    "Dime un dato curioso sobre los mecanismos de la tecnología humana.",
    "Haz un poco de freestyle.",
    f"Dime para que sirve un {keyword}.",
    "Abre el navegador predeterminado porfavor. Ya sea una nueva pestaña si es que ya existe un proceso, o uno proceso si es que no hay.",
    "Escribe unas tres lineas de código python. De lo que sea. (Escribe en el chat, no escribas archivos) (Puedes usar tu sandbox para probar)."
    "Describe resolución de problema matemático, muy sencillo pero con símbolos matemáticos raros."])

simple_voice_assist.request_by_keyword( f"{keyword}. {text}" )
#simple_assist.request(text)

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
if False:
    print("Raw text:", markdown_text)
    if False:
        espeak_manager.speak(markdown.normalize( markdown_text))
    else:
        print("Normalized text:", markdown.normalize( markdown_text) )
    