====
lecs
====
Lightweight Entity Component System for Python

Example usage
=============
.. code:: python

    from lecs.ecs import ECS, Entity, Component, System

    # Create a simple component
    class MooComponent(Component):
        """Data container for cow sounds."""
        def __init__(self):
            super().__init__()
            self.message = 'moo.'

    # Create another simple component, from the MooComponent
    class BullComponent(MooComponent):
        """A bull makes a louder MOO."""
        def __init__(self):
            super().__init__()
            self.message = 'MOO!'

    # Now create a system to handle the components
    class CattleSystem(System):
        def __init__(self, ecs, component_class):
            super().__init__(ecs, component_class)

        def execute(self):
            for component in self.get_component_list():
                print(component.message)


    # Instantiate a base ECS container
    ecs = ECS()


    # Add a new empty entity
    cow = ecs.add_entity()
    # Add a MooComponent to the entity
    cow.add_component(MooComponent())


    # Let's add one more entity
    bull = ecs.add_entity()
    # This one is a bull, so we add the BullComponent
    bull.add_component(BullComponent())

    # We add the CattleSystem. We also add the class name of the component it looks for.
    s = CattleSystem(ecs, ['MooComponent','BullComponent'])

    # We call the System.execute() method.
    s.execute()
