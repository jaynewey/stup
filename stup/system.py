from abc import ABC, abstractmethod
from .family import Family


class System(ABC):
    """Abstract class for processing Entity instances."""
    priority = float("inf")

    def __init__(self, priority=float("inf")):
        self.priority = priority
        self.family = Family(set())

    @abstractmethod
    def update(self, deltatime):
        """The update method that is called every tick.

        :param deltatime: Time between frames. Can be used for framerate independence.
        :type deltatime: float
        :return: None
        """
        pass
