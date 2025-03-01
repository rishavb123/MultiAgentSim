from abc import ABC, abstractmethod
from typing import Any
import uuid


class Entity(ABC):
    def __init__(self):
        self.id = uuid.uuid4()  # Assign a unique ID to each entity

    @abstractmethod
    def update(self, state: Any) -> Any:
        pass

    @property
    def should_remove(self) -> bool:
        return False
