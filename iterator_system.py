from abc import abstractmethod

from ecs.family import Family
from ecs.system import System


class IteratorSystem(System):
    """Utility class for automatically iterating through a family of entities."""

    def __init__(self):
        super().__init__()
        self.family = Family([])

    def update(self):
        """Automatically iterates through the family of the system.

        :return: None
        """
        for entity in self.family:
            self.process(entity)

    @abstractmethod
    def process(self, entity):
        """The method that performs logic on an entity and its components.

        :param entity: The Entity instance that is being processed.
        :type entity: Entity
        :return: None
        """
        pass
