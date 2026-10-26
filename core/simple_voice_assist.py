import threading

# Módulos
from .simple_assist import SimpleAssist
from .speech_to_text import SpeechToText

class SimpleVoiceAssist(SimpleAssist):
    '''
    Tiene para escuchar palabra clave. Se usa en un bucle.
    '''
    def __init__(
        self, keyword: str, stt: SpeechToText, duration_in_seconds: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self._stt = stt
        self._duration_in_seconds = duration_in_seconds

    # Palabra clave
    def normalized_keyword(self):
        return self.keyword.lower().strip()

    def _normalized_text_with_keyword(self, text: str):
        return "".join(char for char in text if char.isalpha() or char == " ")

    def _use_keyword(self, text:str) -> bool:
        keyword = self._normalized_text_with_keyword(text).lower().split()[0]
        print("Key word:", keyword)
        return keyword == self.normalized_keyword()

    def _remove_keyword(self, text:str):
        new_text = ""
        get_first_coincidence = False
        for word in text.split():
            if (
                self._normalized_text_with_keyword(word).lower() == self.normalized_keyword() 
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

    # Using `vosk` and `sounddevice`
    def request_by_microphone(self):
        '''
        Petición por audio.
        '''
        text = self._stt.speech_to_text(self._duration_in_seconds).strip()
        print("STT:", text)
        self.request(text)