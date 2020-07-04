from abc import ABC, abstractmethod


class EntityListener(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def entity_added(self, entity):
        """This method gets called when an entity is added.

        :param entity: The entity that was added
        """
        pass

    @abstractmethod
    def entity_removed(self, entity):
        """This method gets called when an entity is removed.

        :param entity: The entity that was removed
        """
        pass
