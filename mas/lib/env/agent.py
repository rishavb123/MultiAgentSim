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
    def update(self, state: Any) -> None:
        pass

    @property
    def should_remove(self) -> bool:
        return False
