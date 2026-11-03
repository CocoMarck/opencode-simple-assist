import threading, time

# Módulos
from .simple_assist import SimpleAssist
from .speech_to_text import SpeechToText
from .voice_listener import VoiceListener

class SimpleVoiceAssist(SimpleAssist):
    '''
    Tiene para escuchar palabra clave. Se usa en un bucle.
    '''
    def __init__(
        self, stt: SpeechToText, seconds: float, voice_listener: VoiceListener,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stt = stt
        self._seconds = seconds
        
        # Voice listener
        self.voice_listener = voice_listener
        self.voice_listener.on_command = self._on_keyword

        # Flags
        self._wait_keyword = True

    # Palabra clave | Posiblemente todo esto no se use.
    def _normalized_text_with_keyword(self, text: str):
        return "".join(char for char in text if char.isalpha() or char == " ")

    def _use_keyword(self, text:str) -> bool:
        keyword = self._normalized_text_with_keyword(text).lower().split()[0]
        print("Keyword:", keyword)
        return keyword == self.voice_listener.normalized_keyword

    def _remove_keyword(self, text:str):
        new_text = ""
        get_first_coincidence = False
        for word in text.split():
            if (
                self._normalized_text_with_keyword(word).lower() == self.voice_listener.normalized_keyword 
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
    def request_by_stt(self):
        '''
        Petición por audio.
        '''
        text = self._stt.sync_recording_with_seconds(self._seconds).strip()
        print("STT:", text)
        self.request(text)
    
    # Loop temporal
    def _on_keyword(self, text: str):
        print(f"Keyword detected. First captured text `{text}` (ignored). Keyword: `{self.voice_listener.keyword}`")
        self._wait_keyword = False
    
    def loop(self):
        '''
        Esta func hace muchas cosas. Lo mejor seria algo que solo retorne señales, sin while, sin el loop en si, eso que lo maneje otro modulo.
        '''
        self.voice_listener.start()
        try:
            while True:
                time.sleep(1)
                
                if self._wait_keyword:
                    print("Waiting keyword...")
                else:
                    print("\n----------")
                    print(f"Speech to text, you have {self._seconds} seconds to speak.")
                    self.voice_listener.stop()
                    text = self._stt.sync_recording_with_seconds(self._seconds).strip()
                    print("text:", text)
                    print("----------\n")
                    self.request(text)
                    self.voice_listener.start()
                    self._wait_keyword = True
        except KeyboardInterrupt:
            self.voice_listener.stop()
            self._wait_keyword = False
            

            