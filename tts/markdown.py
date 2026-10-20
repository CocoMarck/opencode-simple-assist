import re

'''
Funciones sueltas: Sirve para que un texto markdown, pueda ser leído por cualquier tts.
Quita caracteres que no aportan a la lectura del TTS.

Se puede usar `Regex`, compilados perezosos (lazy). Ejemplo `re.compile(pattern, re.DOTALL)`

El speak normalmente tiene de default `en`. Y lo que se tiene de default, es lo que puede leer mas símbolos sean matemáticos. Pasar a idioma `en`, cuando se detecten símbolos raros, que si aportan a la lectura.
'''

CHARACTER_LIMIT = 100
WORD_LIMIT = 1000
CODE_BLOCK_PATTERN = r"```.*?```"

TAG_BLOCK_PATTERN = r"<([A-Za-z][A-Za-z0-9:_-]*)\b[^>]*>.*?</\1>" # Para `contenido` de `<tag>contenido</tag>`.
TAG_STANDLONE_PATTERN = r"</?[A-Za-z][^>]*>" # Para esto `<tag>` `</tag>`

LATIN_SYMBOLS = [
    "?", "¿", ".", ":", ";", ",", "(", ")", "!", "¡", "&"]
MATHEMATICAL_SYMBOLS = [
    # Básicos Mas Menos
    "+", "-", "−",

    # Básicos Producto
    "⋅", "×",

    # Básicos División
    "÷", "/",

    # Básicos Comparadores
    "=", ">", "<", "≠", "≥", "≤", "⩲", "±", "±",

    # Básicos Porcentaje
    "%", "‰",

    # Básicos Potencias
    "√",                       

    # Álgebra
    "∆", "∑",
    
    # Sin ordenar
    "⊘", "∈", "□", "∎", "≔", "ℝ", "⊹"
]

math_symbols_tags = {
    "⊘": "circled division slash", "∈": "belonging", 
    "□": "tombstone", "∎": "tombstone", "≔": "defined as", "ℝ": "number line", 
    "⊹": "transposed conjugate matrix"
}

def get_allowed_special_characters() -> list[str]:
    '''
    Retorna una lista de caracteres sin caracteres repetidos.
    '''
    return list(set(LATIN_SYMBOLS + MATHEMATICAL_SYMBOLS))
    
def normalize(text:str) -> str:
    '''
    Normalizar texto, algo legible para el TTS.
    '''
    text_without_code = replace_code_blocks(text)
    text_without_tags = remove_tags(text_without_code)
    limit_text = limit_long_text(text_without_tags)
    limit_words = limit_long_words(limit_text)
    text_with_redeable_math_symbols = replace_math_symbols(limit_words)
    return readable_text_only(text_with_redeable_math_symbols).lower()

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
    if long_text(text):
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
def get_tags(text: str) -> list[str]:
    '''
    Obtiene lineas tipo `<tag>contenido</tag>.`
    `<tag>` individuales, y su `contenido`.
    '''
    blocks = [ 
        m.group(0) 
        for m in re.finditer(TAG_BLOCK_PATTERN, text, flags=re.DOTALL | re.IGNORECASE) ]
    singles = [
        m.group(0) 
        for m in re.finditer(TAG_STANDLONE_PATTERN, text, flags=re.IGNORECASE) ]
    tags = []
    tags.extend(blocks)
    tags.extend(singles)
    return tags

def remove_tags(text: str) -> str:
    for i in get_tags(text):
        text = text.replace(i, "")
    return text

# Solo texto legible
def readable_text_only(string: str):
    '''
    Limita el string, a solo texto legible.

    - Espacios.
    - ABC, Español (solo tiene la ñ como adicional).
    - Caracteres chinos, o rusos, o árabes, o etc. Eso si lenguas muertas no.
    - Puntuación (Latin languages): `¿? . , : ;`
    '''
    readable_text_only = ""
    for char in string:
        if (
            char.isalnum() or char.isspace() or 
            (char in get_allowed_special_characters()) ):
            readable_text_only += char
    return readable_text_only

# Símbolos matemáticos raros remplazados por texto legible.
def replace_math_symbols(text: str):
    for key in math_symbols_tags.keys():
        text = text.replace(key, math_symbols_tags[key])
    return text