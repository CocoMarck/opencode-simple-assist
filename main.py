import os
import sys
import subprocess
from datetime import datetime
import json
import random
import re

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
print(assist_session)

def exists_session(session) -> bool:
    '''
    Detecta si existe session
    '''
    result = subprocess.run([
        "opencode", "session", "list", "--format", "json"
    ], capture_output=True, text=True)
    text = result.stdout
    print(text)
    if text:
        return True
    else:
        return False
exists = exists_session(assist_session)
print( "Exists session:", exists )

ID_CHARACTERS = 30
def get_session_id(session) -> str:
    '''
    Obtiene id session, si no existe crash.
    '''
    result = subprocess.run([
        "opencode", "session", "list", "--format", "json"
    ], capture_output=True, text=True)
    session_list = json.loads(result.stdout)
    print(session_list)
    identifier = None
    for item in session_list:
        if item["title"] == session:
            identifier = item["id"]
            break
    if identifier == None:
        raise Exception("The session title not exists")
    else:
        return identifier
session_id = None
if exists:
    session_id = get_session_id(assist_session)
    print("Session ID:", session_id)

# Construcción de prompt con `Speech to Text`
prompt = random.choice([
    f"{key_word}, dime una frase aleatoria por favor.",
    f"{key_word}. Dime un dato curioso sobre los seres vivos.",
    f"{key_word} dime un dato curioso sobre los mecanismos de la tecnología humana.",
    f"{key_word}, haz un poco de freestyle.",
    f"{key_word}, dime para que sirven un {key_word}."])


# Comando a ejecutar, con sesión fija del dia
print("Prompt:", prompt)
def run_prompt(prompt):
    if not use_key_word(prompt):
        raise Exception("Not using the key word")
    normalized_prompt = remove_key_word(prompt)
    print("Normalized prompt: ", normalized_prompt)
    if exists:
        return subprocess.run([
            "opencode", "run", "--session", session_id, normalized_prompt
        ], stdout=subprocess.PIPE)
    else:
        return subprocess.run([
            "opencode", "run", "--title", assist_session, normalized_prompt
        ], stdout=subprocess.PIPE)


# Leer output con `Text to Speech`
def normalize_text_to_speech(text:str) -> str:
    '''
    Normalizar texto, algo legible para el TTS.
    '''
    print("Raw text:", text)
    normalized_text = ""
    for char in text:
        if char.isalnum() or char == " ":
            normalized_text += char
    return normalized_text

def run_text_to_speech(text: str):
    espeak_command = f"espeak-ng -v es '{text}'"
    print(espeak_command)
    os.system(espeak_command)

# Debug
result = run_prompt(prompt)
run_text_to_speech( normalize_text_to_speech(result.stdout.decode('utf-8')) )
