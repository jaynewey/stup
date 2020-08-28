from abc import ABC, abstractmethod
from .family import Family


class System(ABC):
    """Abstract class for processing Entity instances."""
    _priority = float("inf")

    def __init__(self, priority=0):
        self._priority = priority
        self.family = Family(set())

    @property
    def priority(self):
        return self._priority

    @abstractmethod
    def update(self, deltatime):
        """The update method that is called every tick.

        :param deltatime: Time between frames. Can be used for framerate independence.
        :type deltatime: float
        :return: None
        """
        pass
