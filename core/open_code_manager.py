from pathlib import Path
import subprocess, json

class OpenCodeManager:
    '''
    Simple, prácticamente solo maneja sesiones por title.

    El subprocess de run, sera con los parámetros/flags: check, capture_output, text, y un timeout, para que no espere al infinito.
    
    El timeout sera un arma de doble filo, ya que si se le pide abrir algo, y por `x` o `y` razón no puede, o se tarda, sera un problema.

    Los comandos se basan completamente en trabajar con el `workdir`.
    '''
    def __init__(self, timeout: float, workdir: Path):
        self._timeout = timeout
        self._workdir = workdir
    
    def get_session_list(self) -> [dict]:
        '''
        Obtiene en formato lista de dicts, usando el directorio de trabajo, las sesiones disponibles.
        '''
        result = subprocess.run([
            "opencode", "session", "list", "--format", "json"],
            capture_output=True, text=True, cwd=self._workdir)
        return json.loads(result.stdout)
    
    def exists_session_by_id(self, id: str) -> bool:
        session_list = self.get_session_list()
        #print(session_list)
        exists = False
        for item in session_list:
            if item["id"] == id:
                exists = True
                break
        return exists

    def exists_session_by_title(self, title: str) -> bool:
        '''
        Detecta si existe session por su titulo.
        Solo la primera coincidencia. (OpenCode maneja sesiones por ID, y se pueden repetir títulos)
        '''
        session_list = self.get_session_list()
        exists = False
        for item in session_list:
            if item["title"] == title:
                exists = True
                break
        return exists

    def get_session_id_by_title(self, title:str) -> str:
        '''
        Obtiene id session por primera coincidencia con titulo, si no existe crash.
        '''
        session_list = self.get_session_list()
        #print(session_list)
        identifier = None
        for item in session_list:
            if item["title"] == title:
                identifier = item["id"]
                break
        if identifier == None:
            raise Exception("The session title not exists")
        else:
            return identifier

    def run_by_title(self, title:str, prompt:str) -> subprocess:
        '''
        Simple. Crea sesiones. Si ya existe la session con ese titulo, igual crea una nueva.
        '''
        return subprocess.run([
            "opencode", "run", "--dir", self._workdir, "--title", title, prompt], 
            capture_output=True, text=True, timeout=self._timeout)
    
    def run_by_id(self, session_id:str, prompt: str):
        '''
        Simple. Usa sesiones. Si no existe ese ID, crash.
        '''
        return subprocess.run([
            "opencode", "run", "--dir", self._workdir, "--session", session_id, prompt], 
            capture_output=True, text=True, timeout=self._timeout)

