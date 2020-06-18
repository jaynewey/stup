from .entity import Entity
from .family import Family


class EntityManager:
    """Class responsible for handling Entities, their Components and Systems."""

    def __init__(self):
        self._components = {}
        self._systems = []
        self._families = {}

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
            # update all relevant families
            for family in self._families.keys():
                if type(component) in family:
                    self._update_family(family)

    def remove_component_from_entity(self, entity, component_type):
        """Removes all Component instances of given Component type from given Entity instance.

        :param entity: The Entity to have components removed from
        :type entity: Entity
        :param component_type: The Component types to removed from the Entity.
        :return: None
        """
        if component_type in self._components.keys():
            del self._components[component_type][entity]
        # remove entity only from relevant families
        for family in self._families.keys():
            if component_type in family:
                self._families[family].remove(entity)

    def get_family(self, component_types):
        """Returns entities in the map that have all of the given Component types.

        :param component_types: A Set of Component types that you want the Family for.
        :return: The Family of entities that have all of the requested Component types.
        :rtype: Family
        """
        if component_types in self._families.keys():
            return self._families[component_types]
        else:
            entities_all_of = set.intersection(*[set(self._components[component_type].keys()) for component_type in component_types])
            self._families[component_types] = Family(entities_all_of)
            return self._families[component_types]

    def _update_family(self, component_types):
        self._families[component_types].set_entities(set.intersection(*[set(self._components[component_type].keys()) for component_type in component_types]))

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

    def update(self, deltatime):
        """Updates all systems in the database by calling their update functions. Should be called every tick.

        :param deltatime: Time between frames. Can be used for framerate independence.
        :type deltatime: float
        :return: None
        """
        for system in self._systems:
            system.update(deltatime)
