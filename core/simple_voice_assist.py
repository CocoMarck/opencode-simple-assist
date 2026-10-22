
# Módulos
from .simple_assist import SimpleAssist

class SimpleVoiceAssist(SimpleAssist):
    def __init__(
        self, keyword: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword

    # Palabra clave
    def _normalized_text_with_keyword(self, text: str):
        return "".join(char for char in text if char.isalpha() or char == " ")

    def _use_keyword(self, text:str) -> bool:
        keyword = self._normalized_text_with_keyword(text).lower().split()[0]
        print("Key word:", keyword)
        return keyword == self.keyword.lower()

    def _remove_keyword(self, text:str):
        new_text = ""
        get_first_coincidence = False
        for word in text.split():
            if (
                self._normalized_text_with_keyword(word).lower() == self.keyword.lower() 
                and not get_first_coincidence):
                get_first_coincidence = True
            else:
                new_text += f"{word} "
        return new_text[:-1]
    
    # Tipos de peticiones
    def request_by_keyword(self, text: str):
        '''
        Petición de texto, solo habilitada con palabra clave.
        '''
        if not self._use_keyword(text):
            return
        normalized_text = self._remove_keyword(text)
        print("Text:", text)
        print("Normalized text:", normalized_text)
        self.request(normalized_text)