from abc import ABC, abstractmethod


class EntityListener(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def entity_added(self, entity):
        pass

    @abstractmethod
    def entity_removed(self, entity):
        pass
