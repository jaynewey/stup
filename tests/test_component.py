import pytest
from stup.entity_manager import EntityManager
from stup.component import Component


def test_add_component():
    entity_manager = EntityManager()
    entity = entity_manager.create_entity()
    component = Component()
    entity_manager.add_component_to_entity(entity, component)
    assert entity_manager.get_entity_components(entity) == {component}


def test_remove_component():
    entity_manager = EntityManager()
    entity = entity_manager.create_entity()
    component = Component()
    entity_manager.add_component_to_entity(entity, component)
    entity_manager.remove_component_from_entity(entity, type(component))
    assert entity_manager.get_entity_components(entity) == set()


def test_component_map():
    entity_manager = EntityManager()
    entity = entity_manager.create_entity()
    component = Component()
    entity_manager.add_component_to_entity(entity, component)
    assert entity_manager.get_component_map(type(component)) == {entity: component}
