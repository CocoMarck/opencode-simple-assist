from datetime import datetime, timedelta
import subprocess

# Módulos
from tts import markdown
from .open_code_manager import OpenCodeManager
from .espeak_manager import EspeakManager

class SimpleAssist:
    '''
    - Envía el input al AI.
    - Habla la respuesta del AI
    - Tiene memoria en utilizando sesiones.
    - Utiliza modelo especifico, y si no existe, usa el default.
    '''
    def __init__(
        self, open_code_manager: OpenCodeManager, espeak_manager: EspeakManager, memory_in_days: int, model: str):
        self.open_code_manager = open_code_manager
        self.espeak_manager = espeak_manager
        self.memory_in_days = memory_in_days
        self._model = model
    
    # Modelo AI
    def get_model(self) -> str:
        '''
        Obtiene el modelo, si no existe retorna el default.
        '''
        if self.open_code_manager.exist_model(self._model):
            return self._model
        return ""

    # Datetime y sesión
    def _normalize_datetime(self, value: datetime):
        '''
        Ejemplo: `2026-07-25`
        '''
        return value.strftime('%Y-%m-%d')
    
    def _build_datetime_string(self, value: datetime):
        return f"assist-{self._normalize_datetime(value)}"

    def _get_today_session_title(self):
        '''
        Legacy, ya no se usa.
        '''
        return self._build_datetime_string(datetime.today())

    def _get_memory_session_titles(self) -> list[str]:
        '''
        Obtener las sesiones del día en memoria, con for.
        '''
        titles = []
        for i in range(0, self.memory_in_days):
            titles.append( 
                self._build_datetime_string(
                datetime.today()+timedelta(days=-(i) )) )
        return titles
    
    # Resultado del opencode
    def _normalize_strip_result(self, func: subprocess.run, *args, **kwargs) -> str:
        try:
            result = func(*args, **kwargs)
        except subprocess.TimeoutExpired as exc:
            print(exc)
            return "Timeout exception error."
        except subprocess.CalledProcessError as exc:
            print(exc)
            return f"Bad call error. ({exc})"
        return result.stdout.strip()
    
    # Función principal
    def request(self, text:str):
        '''
        - Obtiene o crea sesión de asistente.
        - Manda el texto a open code.
        - Habla la respuesta de open code.
        '''
        # Saber si existe sesión en memoria. Usar la ultima sesión disponible.
        memory_session_titles = self._get_memory_session_titles()
        session_title = ""
        session_exist = False
        for index in range(len(memory_session_titles)-1, -1, -1):
            session_title = memory_session_titles[index]
            session_exist = self.open_code_manager.exists_session_by_title(session_title)
            if session_exist:
                break

        # Usar o crear sesión
        print(f"Session title: {session_title}")
        strip_result = None
        if session_exist:
            print("Existe la sesión")
            session_id = self.open_code_manager.get_session_id_by_title(session_title)
            print(f"Session id: {session_id}")
            
            strip_result = self._normalize_strip_result(
                self.open_code_manager.run_by_id, session_id=session_id, prompt=text, model=self.get_model())
        else:
            print("No existe la sesión, creando una nueva.")
            strip_result = self._normalize_strip_result(
                self.open_code_manager.run_by_title, title=session_title, prompt=text, model=self.get_model())

        print(f"Raw result: \n{strip_result}\n")
        self.espeak_manager.speak( markdown.normalize(strip_result) )