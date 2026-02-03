from abc import ABC, abstractmethod


class BaseChallenge(ABC):
    @abstractmethod
    def check_completion(self) -> bool:
        """Checks if the challenge has been completed."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Returns a human-readable description of the challenge."""
        pass


class DummyChallenge(BaseChallenge):
    def __init__(self, name: str = "Dummy Challenge"):
        self.name = name

    def check_completion(self) -> bool:
        # Simplification: Always returns True for this prototype
        return True

    def get_description(self) -> str:
        return f"This is a {self.name}. Press advance to continue."
