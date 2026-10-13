import random

# Módulos
from core.open_code_manager import OpenCodeManager
from core.espeak_manager import EspeakManager
from core.simple_voice_assist import SimpleVoiceAssist
from tts import markdown

# Palabra clave, para recibir ordenes.
key_word = "Asistente"

# Inicializar módulos
open_code_manager = OpenCodeManager()
espeak_manager = EspeakManager()
simple_voice_assist = SimpleVoiceAssist(key_word, open_code_manager, espeak_manager)

# Construcción de prompt con `Speech to Text`
prompt = random.choice([
    f"{key_word}, dime una frase aleatoria por favor.",
    f"{key_word}. Dime un dato curioso sobre los seres vivos.",
    f"{key_word} dime un dato curioso sobre los mecanismos de la tecnología humana.",
    f"{key_word}, haz un poco de freestyle.",
    f"{key_word}, dime para que sirve un {key_word}."])

simple_voice_assist.request_by_text(prompt)
