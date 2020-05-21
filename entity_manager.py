from entity import Entity


class EntityManager:
    """Class responsible for handling Entities, their Components and Systems."""

    def __init__(self):
        self._components = {}
        self._systems = []

    @staticmethod
    def create_entity():
        """ Creates a new Entity instance and returns it. Alternative to manually creating an Entity instance.

        :return: A new Entity instance. Equivalent to creating an instance manually.
        :rtype: Entity
        """
        return Entity()

    def remove_entity(self, entity):
        """Removes an Entity instance from the Entity Manager.

        :param entity: The Entity instance to be removed from the Entity Manager.
        :type entity: Entity
        :return: None
        """
        for component_type in self._components.keys():
            if entity in component_type:
                del self._components[component_type][entity]

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

    def remove_component_from_entity(self, entity, component_type):
        """Removes all Component instances of given Component type from given Entity instance.

        :param entity: The Entity to have components removed from
        :type entity: Entity
        :param component_type: The Component types to removed from the Entity.
        :return: None
        """
        if component_type in self._components.keys():
            del self._components[component_type][entity]

    def get_entities_for(self, all_of=()):
        """Returns entities in the map that have all of the given Component types.

        :param all_of: List of all Component types that the entities must have.
        :return: A list of Entity instances that have all of the requested component types.
        :rtype: list
        """
        if len(all_of) > 0:
            entities_all_of = set.intersection(*[set(self._components[component_type].keys()) for component_type in all_of])
            return entities_all_of

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

    def update(self):
        """Updates all systems in the database by calling their update functions. Should be called every tick.

        :return: None
        """
        for system in self._systems:
            system.update()
