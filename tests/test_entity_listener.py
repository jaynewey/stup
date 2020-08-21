import pytest
from stup.entity_manager import EntityManager
from stup.entity_listener import EntityListener
from stup.entity import Entity
from stup.component import Component


class TestListener(EntityListener):

    def __init__(self):
        super(TestListener, self).__init__()
        self.event_queue = []

    def entity_added(self, entity):
        self.event_queue.append(("entity_added", entity))

    def entity_removed(self, entity, components):
        self.event_queue.append(("entity_removed", entity, components))


def test_add_listener():
    entity_manager = EntityManager()
    test_listener = TestListener()
    entity_manager.add_listener(test_listener)
    assert test_listener in entity_manager._listeners


def test_remove_listener():
    entity_manager = EntityManager()
    test_listener = TestListener()
    entity_manager.add_listener(test_listener)
    assert test_listener in entity_manager._listeners
    entity_manager.remove_listener(test_listener)
    assert test_listener not in entity_manager._listeners


def test_listener_entity_added():
    entity_manager = EntityManager()
    test_listener = TestListener()
    entity_manager.add_listener(test_listener)
    entity = entity_manager.create_entity()
    assert test_listener.event_queue[-1] == ("entity_added", entity)
    entity = Entity()
    entity_manager.add_entity(entity)
    assert test_listener.event_queue[-1] == ("entity_added", entity)


def test_listener_entity_removed():
    entity_manager = EntityManager()
    test_listener = TestListener()
    entity_manager.add_listener(test_listener)
    entity = entity_manager.create_entity()
    entity_manager.remove_entity(entity)
    assert test_listener.event_queue[-1] == ("entity_removed", entity, set())
    entity = entity_manager.create_entity()
    component = Component()
    entity_manager.add_component_to_entity(entity, component)
    entity_manager.remove_entity(entity)
    assert test_listener.event_queue[-1] == ("entity_removed", entity, set([component]))
