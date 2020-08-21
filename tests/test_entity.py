import pytest
from stup.entity_manager import EntityManager
from stup.entity import Entity


def test_create_entity():
    entity_manager = EntityManager()
    entity = entity_manager.create_entity()
    assert entity_manager.entity_exists(entity)


def test_add_entity():
    entity_manager = EntityManager()
    entity = Entity()
    entity_manager.add_entity(entity)
    assert entity_manager.entity_exists(entity)


def test_remove_entity():
    entity_manager = EntityManager()
    entity = entity_manager.create_entity()
    assert entity_manager.entity_exists(entity)
    entity_manager.remove_entity(entity)
    assert not entity_manager.entity_exists(entity)
