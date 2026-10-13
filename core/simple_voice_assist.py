from datetime import datetime

# Módulos
from tts import markdown
from .open_code_manager import OpenCodeManager
from .espeak_manager import EspeakManager

class SimpleVoiceAssist:
    def __init__(
        self, key_word: str, open_code_manager: OpenCodeManager, espeak_manager: EspeakManager):
        self.key_word = key_word
        self.open_code_manager = open_code_manager
        self.espeak_manager = espeak_manager
    
    def _get_assist_session_title(self):
        return f"assist-{datetime.today().strftime('%Y-%m-%d')}"

    # Palabra clave
    def _normalized_text_with_key_word(self, text: str):
        return "".join(char for char in text if char.isalpha() or char == " ")

    def _use_key_word(text:str):
        key_word = self._normalized_text_with_key_word(text).lower().split()[0]
        print("Key word:", key_word)
        return key_word == key_word.lower()

    def _remove_key_word(self, text:str):
        new_text = ""
        get_first_coincidence = False
        for word in text.split():
            if (
                self._normalized_text_with_key_word(word).lower() == self.key_word.lower() 
                and not get_first_coincidence):
                get_first_coincidence = True
            else:
                new_text += f"{word} "
        return new_text[:-1]
    
    # Peticiones de voz a texto.
    def request_by_text(self, prompt: str):
        normalized_prompt = self._remove_key_word(prompt)
        print("Prompt:", prompt)
        print("Normalized prompt:", normalized_prompt)

        session_title = self._get_assist_session_title()
        exists_session = self.open_code_manager.exists_session_by_title(session_title)
        print(f"Session title: {session_title}")
        result = None
        if exists_session:
            print("Existe la sesión")
            session_id = self.open_code_manager.get_session_id_by_title(session_title)
            print(f"Session id: {session_id}")
            
            result = self.open_code_manager.run_by_id( 
                session_id, normalized_prompt)
        else:
            print("No existe la sesión, creando una nueva.")
            result = self.open_code_manager.run_by_title( 
                session_title, normalized_prompt)

        self.espeak_manager.speak( 
            markdown.normalize(result.stdout.decode('utf-8')) )