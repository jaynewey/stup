class Family:
    def __init__(self, entities):
        self._entities = entities

    def set_entities(self, entities):
        self._entities = entities

    def __iter__(self):
        for entity in self._entities:
            yield entity
