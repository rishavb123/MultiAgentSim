from abc import ABC, abstractmethod
from typing import Any
import uuid


class Agent(ABC):
    def __init__(self):
        self.id = uuid.uuid4()  # Assign a unique ID to each agent

    @abstractmethod
    def observe(self, state: Any) -> Any:
        pass

    @abstractmethod
    def compute_action(self, observation: Any) -> Any:
        pass

    @abstractmethod
    def update(self, state: Any, observation: Any) -> None:
        pass

    def should_kill(self) -> bool:
        return False
    
    def kill(self):
        pass
