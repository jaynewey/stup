from abc import ABC, abstractmethod


class EntityListener(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def entity_added(self, entity):
        """This method gets called when an entity is added to a manager this listener is registered to.

        :param entity: The entity that was added
        """
        pass

    @abstractmethod
    def entity_removed(self, entity, components):
        """This method gets called when an entity is removed from a manager this listener is registered to.

        :param entity: The entity that was removed
        :type entity: Entity
        :param components: The components that were attached to the entity in the system. {type(component): component}
        :type components: dict
        """
        pass
