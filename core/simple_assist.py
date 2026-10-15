from datetime import datetime
import subprocess

# Módulos
from tts import markdown
from .open_code_manager import OpenCodeManager
from .espeak_manager import EspeakManager

class SimpleAssist:
    def __init__(
        self, open_code_manager: OpenCodeManager, espeak_manager: EspeakManager):
        self.open_code_manager = open_code_manager
        self.espeak_manager = espeak_manager

    def _get_assist_session_title(self):
        return f"assist-{datetime.today().strftime('%Y-%m-%d')}"
    
    def _normalize_strip_result(self, func: subprocess.run, *args, **kwargs) -> str:
        try:
            result = func(*args, **kwargs)
        except subprocess.TimeoutExpired as exc:
            print(exc)
            return "Timeout exception error."
        except subprocess.CalledProcessError as exc:
            print(exc)
            return "Bad call error."
        return result.stdout.strip()

    
    def request(self, text:str):
        '''
        - Obtiene o crea sesión de asistente.
        - Manda el texto a open code.
        - Habla la respuesta de open code.
        '''
        session_title = self._get_assist_session_title()
        exists_session = self.open_code_manager.exists_session_by_title(session_title)
        print(f"Session title: {session_title}")
        strip_result = None
        if exists_session:
            print("Existe la sesión")
            session_id = self.open_code_manager.get_session_id_by_title(session_title)
            print(f"Session id: {session_id}")
            
            strip_result = self._normalize_strip_result(
                self.open_code_manager.run_by_id, session_id=session_id, prompt=text)
        else:
            print("No existe la sesión, creando una nueva.")
            strip_result = self._normalize_strip_result(
                self.open_code_manager.run_by_title, title=session_title, prompt=text)

        print(f"Raw result: \n{strip_result}\n")
        self.espeak_manager.speak( markdown.normalize(strip_result) )