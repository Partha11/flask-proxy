from abc import ABC, abstractmethod

class NERPredictor(ABC):
    @abstractmethod
    def predict(self, tasks: list[dict]) -> list[dict]:
        pass
