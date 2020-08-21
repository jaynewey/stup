from stup.entity_listener import EntityListener


class EventListener(EntityListener):
    event_queue = []

    def entity_added(self, entity):
        self.event_queue.append(("entity_added", entity))

    def entity_removed(self, entity, components):
        self.event_queue.append(("entity_removed", entity, components))
