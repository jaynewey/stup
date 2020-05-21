import uuid


class Entity:
    """Simple holders of Universally Unique Identifiers (UUIDs) used to identify this Entity in the Entity Manager."""
    def __init__(self):
        self.uuid = uuid.uuid4()
