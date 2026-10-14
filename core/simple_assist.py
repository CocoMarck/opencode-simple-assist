from datetime import datetime

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
    
    def request(self, text:str):
        '''
        - Obtiene o crea sesión de asistente.
        - Manda el texto a open code.
        - Habla la respuesta de open code.
        '''
        session_title = self._get_assist_session_title()
        exists_session = self.open_code_manager.exists_session_by_title(session_title)
        print(f"Session title: {session_title}")
        result = None
        if exists_session:
            print("Existe la sesión")
            session_id = self.open_code_manager.get_session_id_by_title(session_title)
            print(f"Session id: {session_id}")
            
            result = self.open_code_manager.run_by_id( 
                session_id=session_id, prompt=text)
        else:
            print("No existe la sesión, creando una nueva.")
            result = self.open_code_manager.run_by_title( 
                title=session_title, prompt=text)

        self.espeak_manager.speak( 
            markdown.normalize(result.stdout.decode('utf-8')) )