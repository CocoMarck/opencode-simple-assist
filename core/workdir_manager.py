import os
import shutil
from pathlib import Path

from core.agent_manager import AgentManager

APP_DIR = "simple_assist"

class WorkdirManager:
    def __init__( self, root: Path, agent_manager: AgentManager):
        self._workdir = root
        self._agent_manager = agent_manager
        self._agents_file = self._workdir.joinpath("AGENTS.md")
        
    @property # Esto es para que jale como propiedad. Como si fuera code `C`.
    def workdir(self) -> Path:
        return self._workdir
    
    def ensure(self) -> Path:
        '''
        Crear el directorio si no existe, y lo devuelve
        '''
        self._workdir.mkdir(parents=True, exist_ok=True)
        self._save_agents_file()
        return self._workdir
    
    def _save_agents_file(self):
        if not self._agents_file.exists():
            self._write_agents_file()
    
    def _write_agents_file(self):
        with open(self._agents_file, "w") as file:
            file.write( self._agent_manager.render_agents_md() )
