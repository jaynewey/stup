# stup-ecs
A tiny, simple to use, lightweight Python Entity Component System. Fully functioning and usable for small practice projects. In development. Not recommended for production code.

# Usage
## Entity
Entities are are Universally Unique Identifiers (UUIDs) and nothing else. Entities can be instantiated directly:
```
entity = Entity()
```
or through the Entity Manager:
```
entity = EntityManager.create_entity()
```

## EntityManager
The Entity Manager is responsible for handling Entities, their Components and Systems. It is essentially a database of all Entities and Systems and is the link between Entities and their Components.  
You will usually want to create an instance of an Entity Manager:
```
entity_manager = EntityManager()
```
...And call its `update()` function every tick. This updates all of the Systems registered with the Entity Manager.
Entities are not registered in the Entity Manager database at all unless they have Components attached to them.

## Component
Components are simply data holders and nothing more. You should inherit the Component class when writing Components. Components should not contain logic and should only contain data.  
An example Position Component class in a 2d game could be:
```
class PositionComponent(Component):  
	def __init__(self):
		self.x = 0
		self.y = 0
```
However you might prefer to use private attributes with getter/setter functions.
### Adding and Removing Components
You can add and remove components from entities dynamically through the Entity Manager:
```
entity = Entity()
entity_manager = EntityManager()
entity_manager.add_component_to_entity(entity, PositionComponent())
entity_manager.remove_component_from_entity(entity, PositionComponent)
```
Notice that you must provide a Component instance when adding a Component but only need provide a Component type when removing one.
## System
Systems are for processing specific sets of Entities. You should inherit the `System` class when writing Systems. The `update()` method of your System is called every tick and should perform your logic, usually iterating through the `entities` set. The `entities` set is a set of `Entity` instances and should be assigned in the constructor.  
Usually in a System you want to only perform logic on Entities that have a specific Component type or set of Component types. For example, a Movement System might only affect Entities that have a Position Component and a Velocity Component, in which case you would use the `EntityManager` function `get_entities_for()`.
Then, you would want to work with these components, so use the EntityManager's `get_component_map()` to get all Components of a type so you can access a `Component` by using an `Entity` as the key.  
Here's how it might look:
```
class MovementSystem(System):
	def __init__(self, entity_manager):
		# Get all entities with position and velocity components:
		self.entities = entity_manager.get_entities_for(PositionComponent, VelocityComponent)
		# Get the component maps so we can access the components using the entity as a key:
		self.movement_component_map = entity_manager.get_component_map(MovementComponent)
		self.position_component_map = entity_manager.get_component_map(PositionComponent)
		
	def update(self):
		for entity in self.entities():
			position = self.position_component_map[entity]
			velocity = self.velocity_component_map[entity]
			position.x += velocity.x
			position.y += velocity.y
```
Then, you would want to add an instance of this system to the Entity Manager:
```
movement_system = MovementSystem()
entity_manager.add_system(movement_system)
```
Systems can also be removed dynamically:
```
entity_manager.remove_system(movement_system)
```
