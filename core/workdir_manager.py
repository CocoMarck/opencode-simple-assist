import os
from pathlib import Path

APP_DIR = "simple_assist"

class WorkdirManager:
    def __init__( self, root: Path):
        self._workdir = root
        
    @property # Esto es para que jale como propiedad. Como si fuera code `C`.
    def workdir(self) -> Path:
        return self._workdir
    
    def ensure(self) -> Path:
        '''
        Crear el directorio si no existe, y lo devuelve
        '''
        self._workdir.mkdir(parents=True, exist_ok=True)
        return self._workdir
