import re

'''
Funciones sueltas: Sirve para que un texto markdown, pueda ser leído por cualquier tts.
Quita caracteres que no aportan a la lectura del TTS.

Se puede usar `Regex`, compilados perezosos (lazy). Ejemplo `re.compile(pattern, re.DOTALL)`
'''

CHARACTER_LIMIT = 100
WORD_LIMIT = 1000
CODE_BLOCK_PATTERN = r"```.*?```"
TAG_PATTERN = r"<.*>"
    
def normalize(text:str) -> str:
    '''
    Normalizar texto, algo legible para el TTS.
    '''
    text_without_code = replace_code_blocks(text)
    text_without_tags = remove_tags(text_without_code)
    limit_text = limit_long_text(text_without_tags)
    limit_words = limit_long_words(limit_text)
    normalized_text = ""
    for char in limit_words:
        if char.isalnum() or char == " ":
            normalized_text += char
    return normalized_text.lower()

# Limit long word
def long_word(word: str) -> bool:
    return len(word) > CHARACTER_LIMIT

def limit_long_word(word: str) -> str:
    '''
    Limita palabra al limite de caracteres.
    '''
    if long_word(word):
        return word[:CHARACTER_LIMIT]
    return word

def limit_long_words(text: str) -> str:
    '''
    Limita cantidad de caracteres en las palabras de un texto.
    '''
    new_text = ""
    for word in text.split():
        new_text += limit_long_word(word) + " "
    return new_text[:-1]

# Limit words
def long_text(text: str) -> bool:
    return len(text.split()) > WORD_LIMIT

def limit_long_text(text: str) -> str:
    '''
    Limita cantidad de palabras.
    '''
    if long_word(text):
        new_text = ""
        words = text.split()
        for i in range(0, len(words)):
            if i > WORD_LIMIT:
                break
            new_text += f"{words[i]} "
        return new_text[:-1]
    return text

# Raplace code blocks
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
        text = text.replace(code_block, "\nCode block\n")
    return text

# Remove tags
def get_tags(text: str) -> [str]:
    '''
    Obtiene lineas tipo <tag>, o </tag>.
    '''
    return re.findall(TAG_PATTERN, text)

def remove_tags(text: str) -> str:
    for i in get_tags(text):
        text = text.replace(i, "")
    return text