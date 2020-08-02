from abc import abstractmethod

from .family import Family
from .system import System


class IteratorSystem(System):
    """Utility class for automatically iterating through a family of entities."""

    def __init__(self):
        super().__init__()

    def update(self, deltatime):
        """Automatically iterates through the family of the system.

        :return: None
        """
        for entity in self.family:
            self.process(deltatime, entity)

    @abstractmethod
    def process(self, deltatime, entity):
        """The method that performs logic on an entity and its components.

        :param deltatime: Time between frames. Can be used for framerate independence.
        :type deltatime: float
        :param entity: The Entity instance that is being processed.
        :type entity: Entity
        :return: None
        """
        pass
