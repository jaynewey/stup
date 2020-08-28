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


def test_system_priority():
    entity_manager = EntityManager()
    system_1 = UpdateSystem()
    system_2 = UpdateSystem()
    entity_manager.add_system(system_1, system_2)
    assert entity_manager._systems == [system_1, system_2]
    system_3 = UpdateSystem(1)
    entity_manager.add_system(system_3)
    assert entity_manager._systems == [system_3, system_1, system_2]
    system_4 = UpdateSystem(0)
    entity_manager.add_system(system_4)
    entity_manager.remove_system(system_1)
    assert entity_manager._systems == [system_4, system_3, system_2]
    entity_manager.remove_system(system_4)
    assert entity_manager._systems == [system_3, system_2]
