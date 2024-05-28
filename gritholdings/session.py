from .browser_automation import BrowserAutomation
from .local_db import LocalDB
from .llm import LLM


class Session:
    def __init__(self):
        self._resources = {
            'BrowserAutomation': BrowserAutomation,
            'LocalDB': LocalDB,
            'LLM': LLM
        }

    def resource(self, service_name, **kwargs):
        cls = self._resources.get(service_name)
        if cls is None:
            raise ValueError(f"Class '{service_name}' not found.")
        return cls(**kwargs)