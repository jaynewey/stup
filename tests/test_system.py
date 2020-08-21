import pytest
from stup.entity_manager import EntityManager
from stup.system import System
from .systems import *


def test_add_system():
    entity_manager = EntityManager()
    system = UpdateSystem()
    entity_manager.add_system(system)
    assert system in entity_manager._systems


def test_remove_system():
    entity_manager = EntityManager()
    system = UpdateSystem()
    entity_manager.add_system(system)
    assert system in entity_manager._systems
    entity_manager.remove_system(system)
    assert system not in entity_manager._systems


def test_update_systems():
    entity_manager = EntityManager()
    system = UpdateSystem()
    entity_manager.add_system(system)
    assert system.updates == 0
    entity_manager.update(1)
    assert system.updates == 1
