from pathlib import Path
from jinja2 import Environment

class AgentManager:
    def __init__(self, name: str, environment: Environment):
        self._name = name
        self._environment = environment
    
    def render_agents_md(self) -> list[str]:
        template = self._environment.get_template("simple_assist_agents.md.jinja")
        info = {"name": self._name}
        return template.render(info)