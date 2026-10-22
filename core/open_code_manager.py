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
    
    def get_models(self) -> list[str]:
        '''
        Obtiene una lista de strings de los modelos disponibles.

        Se ven algo asi: `compañia/AI-Chido-2.0`
        '''
        result = subprocess.run(
            ["opencode", "models"], capture_output=True, text=True)
        return list( filter(None, result.stdout.split("\n")) )
    
    def get_models_dict(self) -> dict:
        '''
        Conceptual, debe jalar. Obtiene una dict asi (`dict{ str: list[str]}`):
        ```
        dueño/
            CodeName-Modelo-AI
        ```

        Servirá para selección mas seccionada de modelo, por GUI, o CLI.

        De hecho, puede que sea mejor que no viva en `OpenCodeManager`.
        '''
        models = self.get_models()
        models_dict = {}
        for model in models:
            sections = model.split("/")
            
            # Agregar code name y dueño y subdueños
            owner_and_sub = ""
            code_name = ""
            for index in range(0, len(sections)):
                if index == max(sections):
                    code_name = sections[index]
                else:
                    owner_and_sub += sections[index] + "/"
            
            # Si no existe owner como key, agregarlo como tal. Tiene que ser una lista.
            if not owner_and_sub in models_dict.keys():
                models_dict[owner_and_sub] = []
            
            # Agregar code name.
            models_dict[owner_and_sub].append(code_name)
        return models_dict
    
    def exist_model(self, model: str) -> bool:
        return model in self.get_models()
    
    def get_session_list(self) -> list[dict]:
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

    def run_by_title(self, title:str, prompt:str, model:str = "") -> subprocess:
        '''
        Simple. Crea sesiones. Si ya existe la session con ese titulo, igual crea una nueva.
        '''
        return subprocess.run([
            "opencode", "run", "--dir", self._workdir, "--model", model, "--title", title, prompt], 
            capture_output=True, text=True, timeout=self._timeout)
    
    def run_by_id(self, session_id:str, prompt: str, model:str=""):
        '''
        Simple. Usa sesiones. Si no existe ese ID, crash.
        '''
        return subprocess.run([
            "opencode", "run", "--dir", self._workdir, "--model", model, "--session", session_id, prompt], 
            capture_output=True, text=True, timeout=self._timeout)

