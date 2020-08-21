import pytest
from stup.family import Family
from stup.entity_manager import EntityManager
from .components import *


def test_get_family():
    entity_manager = EntityManager()
    entity = entity_manager.create_entity()
    assert entity not in entity_manager.get_family(PositionComponent)._entities
    entity_manager.add_component_to_entity(entity, PositionComponent())
    assert entity in entity_manager.get_family(PositionComponent)._entities
    assert entity not in entity_manager.get_family(VelocityComponent)._entities
    entity_manager.add_component_to_entity(entity, VelocityComponent())
    assert entity in entity_manager.get_family(PositionComponent, VelocityComponent)._entities


def test_update_family():
    entity_manager = EntityManager()
    entity = entity_manager.create_entity()
    family = entity_manager.get_family(PositionComponent)
    assert entity not in family._entities
    entity_manager.add_component_to_entity(entity, PositionComponent())
    assert entity in family._entities
    entity_manager.remove_component_from_entity(entity, PositionComponent)
    assert entity not in family._entities
