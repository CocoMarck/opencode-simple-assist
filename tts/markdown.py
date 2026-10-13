'''
Funciones sueltas: Sirve para que un texto markdown, pueda ser leído por cualquier tts.

Quita caracteres que no aportan a la lectura del TTS.
'''

WORD_LIMIT = 100
    
def normalize(text:str) -> str:
    '''
    Normalizar texto, algo legible para el TTS.
    '''
    limit_words = limit_long_words(text)
    print("Raw text:", text)
    #print("Limit words:", limit_words)
    normalized_text = ""
    for char in limit_words:
        if char.isalnum() or char == " ":
            normalized_text += char
    return normalized_text

def long_word(word: str) -> bool:
    return len(word) > WORD_LIMIT

def limit_long_word(word: str) -> str:
    '''
    Limita palabra al limite de caracteres.
    '''
    len_word = len(word)
    if len_word > WORD_LIMIT:
        new_word = ""
        for i in range(0, WORD_LIMIT):
            new_text = word[i]
        return new_word
    return word

def limit_long_words(text: str):
    '''
    Limita cantidad de caracteres en las palabras de un texto.
    '''
    new_text = ""
    for word in text.split():
        new_text += limit_long_word(word) + " "
    return new_text[:-1]
