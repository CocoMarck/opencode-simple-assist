'''
Funciones sueltas: Sirve para que un texto markdown, pueda ser leído por cualquier tts.

Quita caracteres que no aportan en un input para leer para el TTS.
'''
    
def normalize(text:str) -> str:
    '''
    Normalizar texto, algo legible para el TTS.
    '''
    print("Raw text:", text)
    normalized_text = ""
    for char in text:
        if char.isalnum() or char == " ":
            normalized_text += char
    return normalized_text