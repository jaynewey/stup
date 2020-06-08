# stup-ecs
A tiny, simple to use, lightweight Python Entity Component System. Fully functioning and usable for small practice projects. In development. Not recommended for production code.

# Usage
## Entity
Entities are are Universally Unique Identifiers (UUIDs) and nothing else. Entities can be instantiated directly:
```python
entity = Entity()
```
or through the entity manager:
```python
entity = EntityManager.create_entity()
```

## EntityManager
The entity manager is responsible for handling entities, their components and systems. It is essentially a database of all entities and systems and is the link between entities and their components.  
You will usually want to create an instance of an `EntityManager`:
```python
entity_manager = EntityManager()
```
...And call its `update()` function every tick. This updates all of the Systems registered with the Entity Manager.
Entities are not registered in the entity manager database at all unless they have components attached to them.

## Component
Components are simply data holders and nothing more. You should inherit the `Component` class when writing components. Components should not contain logic and should only contain data.  
An example position component class in a 2d game could be:
```python
class PositionComponent(Component):  
	def __init__(self):
		self.x = 0
		self.y = 0
```
However you might prefer to use private attributes with getter/setter functions.
### Adding and Removing Components
You can add and remove components from entities dynamically through the Entity Manager:
```python
entity = Entity()
entity_manager = EntityManager()
entity_manager.add_component_to_entity(entity, PositionComponent())
entity_manager.remove_component_from_entity(entity, PositionComponent)
```
Notice that you must provide a `Component` instance when adding a component but only need provide a `Component` type when removing one.
## System
Systems are for processing specific sets of entities. You should inherit the `System` class when writing systems. The `update()` method of your system is called every tick and should perform your logic, usually iterating through a `Family`. A `Family` is ensentially a set of `Entity` instances and should be assigned in the constructor.  
Usually in a System you want to only perform logic on entities that have a specific Component type or set of Component types. For example, a movement system might only affect entities that have a position component and a velocity component, we use families to hold these for us, and we can obtain a `Family` of entities by using `get_family` from an `EntityManager` instance.
Then, you would want to work with the components of the entities, so use `EntityManager`'s `get_component_map()` to get all components of a type so you can access a `Component` by using an `Entity` as the key.  
Here's how it might look:
```python
class MovementSystem(System):
	def __init__(self, entity_manager):
		super().__init__()
		# Get the Family of entities with position and velocity components:
		self.family = entity_manager.get_family((PositionComponent, VelocityComponent))
		# Get the component maps so we can access the components using the entity as a key:
		self.movement_component_map = entity_manager.get_component_map(MovementComponent)
		self.position_component_map = entity_manager.get_component_map(PositionComponent)
		
	def update(self):
		for entity in self.family:
			position = self.position_component_map[entity]
			velocity = self.velocity_component_map[entity]
			position.x += velocity.x
			position.y += velocity.y
```
Then, you can add an instance of this system to the Entity Manager:
```python
movement_system = MovementSystem()
entity_manager.add_system(movement_system)
```
Systems can also be removed dynamically:
```python
entity_manager.remove_system(movement_system)
```

### IteratorSystem

Most systems will involve iterating over a `family`. To avoid redundant code, stup-ecs provides a handy utility class which will do this for you, called `IteratorSystem`.

In the constructor of your `System`, get the `Family` of entities as you normally would:

```python
self.family = entity_manager.get_family((PositionComponent, VelocityComponent))
```

Rather than overriding the `Update()` function, override `Iterator System`'s `Process()`function to do your logic and it will be applied to all entities in the family. The `MovementSystem` from before would look like this:

```python
class MovementSystem(IteratorSystem):
	def __init__(self, entity_manager):
		super().__init__()
		# Get the Family of entities with position and velocity components:
		self.family = entity_manager.get_family((PositionComponent, VelocityComponent))
		# Get the component maps so we can access the components using the entity as a key:
		self.movement_component_map = entity_manager.get_component_map(MovementComponent)
		self.position_component_map = entity_manager.get_component_map(PositionComponent)		

	def process(self, entity):
		position = self.position_component_map[entity]
		velocity = self.velocity_component_map[entity]
		position.x += velocity.x
		position.y += velocity.y
```