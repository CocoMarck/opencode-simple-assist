import os
import sys
import subprocess
from datetime import datetime
import json
import random

# Palabra clave, para recibir ordenes.
key_word = "Asistente"

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
    "Dime una frase aleatoria por favor.", 
    "Dime un dato curioso sobre los seres vivos.",
    "Dime un dato curioso sobre los mecanismos humanos",
    "Haz un poco de freestyle"])

# Comando a ejecutar, con sesión fija del dia
if exists:
    result = subprocess.run([
        "opencode", "run", "--session", session_id, prompt
    ], stdout=subprocess.PIPE)
else:
    result = subprocess.run([
        "opencode", "run", "--title", voice_session, prompt
    ], stdout=subprocess.PIPE)

print("Prompt:", prompt)

# Leer output con `Text to Speech`
def normalize_text(text:str) -> str:
    '''
    Normalizar texto, algo legible para el TTS.
    '''
    print("Raw text:", text)
    normalized_text = ""
    for char in text:
        if char.isalnum() or char == " ":
            normalized_text += char
    return normalized_text


espeak_command = f"espeak-ng -v es '{normalize_text(result.stdout.decode('utf-8'))}'"
print(espeak_command)
os.system(espeak_command)
