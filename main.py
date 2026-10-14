import random

# Módulos
from core.open_code_manager import OpenCodeManager
from core.espeak_manager import EspeakManager
from core.simple_voice_assist import SimpleVoiceAssist
from tts import markdown

# Palabra clave, para recibir ordenes.
keyword = "Asistente"

# Inicializar módulos
open_code_manager = OpenCodeManager()
espeak_manager = EspeakManager()
simple_voice_assist = SimpleVoiceAssist(keyword, open_code_manager, espeak_manager)

# Construcción de prompt con `Speech to Text`
text = random.choice([
    f"{keyword}, dime una frase aleatoria por favor.",
    f"{keyword}. Dime un dato curioso sobre los seres vivos.",
    f"{keyword} dime un dato curioso sobre los mecanismos de la tecnología humana.",
    f"{keyword}, haz un poco de freestyle.",
    f"{keyword}, dime para que sirve un {keyword}.",
    f"{keyword}, abre el navegador predeterminado porfavor. Ya sea una nueva pestaña si es que ya existe un proceso, o uno proceso si es que no hay."])

simple_voice_assist.request_by_keyword(text)
#text = input("Orden a open code: ")
#if text:
    #simple_voice_assist.request(text)
