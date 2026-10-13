import subprocess, json

class OpenCodeManager:
    '''
    Simple, prácticamente solo maneja sesiones por title.
    '''
    def __init__(self):
        pass
    
    def get_session_list(self) -> [dict]:
        result = subprocess.run([
            "opencode", "session", "list", "--format", "json"
        ], capture_output=True, text=True)
        return json.loads(result.stdout)
    
    def exists_session_by_id(self, id: str) -> bool:
        session_list = self.get_session_list()
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
        #print(session_list)
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
            "opencode", "run", "--title", title, prompt], stdout=subprocess.PIPE)
    
    def run_by_id(self, session_id:str, prompt: str):
        '''
        Simple. Usa sesiones. Si no existe ese ID, crash.
        '''
        return subprocess.run([
            "opencode", "run", "--session", session_id, prompt], 
            stdout=subprocess.PIPE)

