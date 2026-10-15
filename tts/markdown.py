import re

'''
Funciones sueltas: Sirve para que un texto markdown, pueda ser leído por cualquier tts.
Quita caracteres que no aportan a la lectura del TTS.

Se puede usar `Regex`, compilados perezosos (lazy). Ejemplo `re.compile(pattern, re.DOTALL)`
'''

WORD_LIMIT = 100
CODE_BLOCK_PATTERN = r"```.*?```"
TAG_PATTERN = r"<.*>"
    
def normalize(text:str) -> str:
    '''
    Normalizar texto, algo legible para el TTS.
    '''
    text_without_tags = remove_tags(text)
    text_without_code = replace_code_blocks(text_without_tags)
    
    limit_words = limit_long_words(text_without_code)
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
    if long_word(word):
        return word[:WORD_LIMIT]
    return word

def limit_long_words(text: str) -> str:
    '''
    Limita cantidad de caracteres en las palabras de un texto.
    '''
    new_text = ""
    for word in text.split():
        new_text += limit_long_word(word) + " "
    return new_text[:-1]

def get_code_blocks(text: str) -> [str]:
    '''
    Obtienes multiline de ```Mucho code```. No detectar como un solo code block, varios.
    '''
    return re.findall(CODE_BLOCK_PATTERN, text, re.DOTALL)

def get_code_line(text: str) -> [str]:
    '''
    Una linea tipo `code`.
    '''
    return re.findall("`.*`", text)

def replace_code_blocks(text: str) -> str:
    '''
    Remplazar bloques de código, con algo legible.
    '''
    for code_block in get_code_blocks(text):
        text = text.replace(code_block, "\nCode Block\n")
    return text

def get_tags(text: str) -> [str]:
    '''
    Obtiene lineas tipo <tag>, o </tag>.
    '''
    return re.findall(TAG_PATTERN, text)

def remove_tags(text: str) -> str:
    for i in get_tags(text):
        text = text.replace(i, "")
    return text
