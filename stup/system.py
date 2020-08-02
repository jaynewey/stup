from abc import ABC, abstractmethod


class System(ABC):
    """Abstract class for processing Entity instances."""
    def __init__(self):
        self.family = Family([])

    @abstractmethod
    def update(self, deltatime):
        """The update method that is called every tick.

        :param deltatime: Time between frames. Can be used for framerate independence.
        :type deltatime: float
        :return: None
        """
        pass
