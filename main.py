import os
import sys
import subprocess
from datetime import datetime
import json
import random
import re

# Módulos
from core.open_code_manager import OpenCodeManager
from tts import markdown

# Inicializar módulos
open_code_manager = OpenCodeManager()

# Palabra clave, para recibir ordenes.
key_word = "Asistente"

def normalized_text_with_key_word(text: str):
    return "".join(char for char in text if char.isalpha() or char == " ")

def use_key_word(text:str):
    key_word = normalized_text_with_key_word(text).lower().split()[0]
    print("Key word:", key_word)
    return key_word == key_word.lower()

def remove_key_word(text:str):
    new_text = ""
    get_first_coincidence = False
    for word in text.split():
        if (
            normalized_text_with_key_word(word).lower() == key_word.lower() and 
            not get_first_coincidence):
            get_first_coincidence = True
        else:
            new_text += f"{word} "
    return new_text[:-1]

# Asegurar sesión fija del dia
assist_session = f"assist-{datetime.today().strftime('%Y-%m-%d')}"
print( "Session:", assist_session)

exists = open_code_manager.exists_session_by_title(assist_session)
print( "Exists session:", exists )

ID_CHARACTERS = 30
session_id = None
if exists:
    session_id = open_code_manager.get_session_id_by_title(assist_session)
    print("Session ID:", session_id)

# Construcción de prompt con `Speech to Text`
prompt = random.choice([
    f"{key_word}, dime una frase aleatoria por favor.",
    f"{key_word}. Dime un dato curioso sobre los seres vivos.",
    f"{key_word} dime un dato curioso sobre los mecanismos de la tecnología humana.",
    f"{key_word}, haz un poco de freestyle.",
    f"{key_word}, dime para que sirve un {key_word}."])


# Comando a ejecutar, con sesión fija del dia
normalized_prompt = remove_key_word(prompt)
print("Prompt:", prompt)
print("Normalized prompt:", normalized_prompt)


# Leer output con `Text to Speech`
def run_text_to_speech(text: str):
    espeak_command = f"espeak-ng -v es '{text}'"
    print(espeak_command)
    os.system(espeak_command)

# Debug
result = open_code_manager.run_prompt_by_title(assist_session, normalized_prompt)
run_text_to_speech( markdown.normalize(result.stdout.decode('utf-8')) )
