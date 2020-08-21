from .entity import Entity
from .family import Family


class EntityManager:
    """Class responsible for handling Entities, their Components and Systems."""

    def __init__(self):
        self._entities = {}  # {entity: {type(component): component}}
        self._components = {}  # {type(component): {entity: component}}
        self._systems = []
        self._families = {}
        self._listeners = []

    def create_entity(self):
        """ Creates a new Entity instance, adds it to the manager and returns it.

        :return: A new Entity instance. Equivalent to creating an instance manually.
        :rtype: Entity
        """
        return self.add_entity(Entity())

    def add_entity(self, entity):
        """Adds an existing Entity instance to the manager and returns it.

        :param entity: The Entity instance to be added
        :return: Entity
        """
        if entity not in self._entities.keys():
            self._entities[entity] = {}
        self._notify_listeners("entity_added", (entity,))
        return entity

    def remove_entity(self, entity):
        """Removes an Entity instance from the Entity Manager.

        :param entity: The Entity instance to be removed from the Entity Manager.
        :type entity: Entity
        :return: A set containing the removed entity's components
        :rtype: set
        """
        removed_components = set()
        for component_type in self._components.keys():
            if entity in self._components[component_type].keys():
                removed_components.add(self._components[component_type][entity])
                del self._components[component_type][entity]
                self._update_families_with_component_type(component_type)
        del self._entities[entity]
        self._notify_listeners("entity_removed", (entity, removed_components))
        return removed_components

    def entity_exists(self, entity):
        """Returns True if the given Entity instance is in the entity manager,

        :param entity: The Entity instance to be checked.
        :type entity: Entity
        :return: A boolean representing whether the Entity was found or not.
        :rtype: bool
        """
        return entity in self._entities.keys()

    def add_component_to_entity(self, entity, *components):
        """Applies given Component instances to a given Entity instance.

        :param entity: The Entity to have components added to.
        :type entity: Entity
        :param components: The Component instances to be added to the entity.
        :return: None
        """
        for component in components:
            component_type = type(component)
            if component_type not in self._components.keys():
                self._components[component_type] = {}
            self._components[component_type][entity] = component
            self._entities[entity][component_type] = component
            # update all relevant families
            self._update_families_with_component_type(component_type)

    def remove_component_from_entity(self, entity, component_type):
        """Removes all Component instances of given Component type from given Entity instance.

        :param entity: The Entity to have components removed from
        :type entity: Entity
        :param component_type: The Component types to removed from the Entity.
        :return: None
        """
        if component_type in self._components.keys():
            del self._components[component_type][entity]
        if component_type in self._entities[entity].keys():
            del self._entities[entity][component_type]
        # remove entity only from relevant families
        self._update_families_with_component_type(component_type)

    def get_family(self, *component_types):
        """Returns entities in the map that have all of the given Component types.

        :param component_types: A Set of Component types that you want the Family for.
        :return: The Family of entities that have all of the requested Component types.
        :rtype: Family
        """
        component_types = frozenset(component_types)
        if component_types in self._families.keys():
            return self._families[component_types]
        elif all([component_type in self._components.keys() for component_type in component_types ]):
            entities_all_of = set.intersection(*[set(self._components[component_type].keys())
                                                 for component_type in component_types])
            self._families[component_types] = Family(entities_all_of)
            return self._families[component_types]
        else:
            self._families[component_types] = Family(set())
            return self._families[component_types]

    def _update_family(self, component_types):
        self._families[component_types].set_entities(set.intersection(*[set(self._components[component_type].keys())
                                                                        for component_type in component_types]))

    def _update_families_with_component_type(self, component_type):
        for family in self._families.keys():
            if component_type in family:
                self._update_family(family)

    def get_entity_components(self, entity):
        """Gets a set of all components attached to the given entity.

        :param entity: The entity instance to get the components of
        :type entity: Entity
        :return: The set of all components attached to the given entity
        :rtype: set
        """
        return {component for component in self._entities[entity].values()}

    def get_component_map(self, component_type):
        """Returns dictionary of key value pairs where Entity instances are the key and Component instances are the
        values and the Component instances are of the given Component type.

        :param component_type: The type of Component
        :return: A dictionary of Entity instances to their Component instances.
        :rtype: dict
        """
        return self._components[component_type]

    def add_system(self, *system):
        """Adds given System instances to the Entity Manager.

        :param system: The System instance to add to the Entity Manager.
        :return: None
        """
        self._systems.extend(system)

    def remove_system(self, system):
        """Removes given System instance from the Entity Manager.

        :param system:  The System instance to remove from the Entity Manager.
        :return: None
        """
        self._systems.remove(system)

    def add_listener(self, listener):
        """Adds a given Listener instance to the Entity Manager.

        :param listener: The Listener instance to add to the Entity Manager.
        :type listener: Listener
        :return: None
        """
        self._listeners.append(listener)

    def remove_listener(self, listener):
        """Removes a given Listener instance from the Entity Manager.

        :param listener: The Listener instance to remove from the Entity Manager.
        :type listener: Listener
        :return: None
        """
        self._listeners.remove(listener)

    def _notify_listeners(self, event, parameters):
        """Notifies the manager's events with the event triggered e.g "entity added".

        :param event: The event triggered
        :type event: str
        :return: None
        """
        for listener in self._listeners:
            getattr(listener, event)(*parameters)

    def update(self, deltatime):
        """Updates all systems in the database by calling their update functions. Should be called every tick.

        :param deltatime: Time between frames. Can be used for framerate independence.
        :type deltatime: float
        :return: None
        """
        for system in self._systems:
            system.update(deltatime)
