class Family:
    """Data structure for tracking sets of entities that have specific Component types."""

    def __init__(self, entities):
        self._entities = entities

    def set_entities(self, entities):
        """

        :param entities: A set of Entity instances.
        :return: None
        """
        self._entities = entities

    def __iter__(self):
        for entity in self._entities:
            yield entity
