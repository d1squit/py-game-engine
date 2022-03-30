from components import *
from typing import TypeVar, Generic

T = TypeVar('T')


class GameObject (Generic[T]):
	def __init__ (self, name: str, tag="", layer=[]):
		self.name = name
		self.tag = tag
		self.layer = layer

		GameObject.unsorted_instances[id(self)] = self

		self.components: list[Component] = []
		self.add_component(Transform(use_meta=True))


# OPERATORS
	def __repr__ (self):
		return f"GameObject (Name: {self.name}, {self.transform})"

	def __str__ (self):
		return f"GameObject (Name: {self.name}, {self.transform})"

	def __del__ (self):
		try: GameObject.sorted_instances.pop(id(self))
		except KeyError: GameObject.unsorted_instances.pop(id(self))
# ---------


# PROPERTIES
	@property
	def transform (self) -> Transform:
		return self.get_component(Transform)
	@transform.setter
	def transform (self, tr: Transform):
		self.get_component(Transform).position = tr.position
		self.get_component(Transform).rotation = tr.rotation
		self.get_component(Transform).scale = tr.scale
# ----------

# STATIC PROPERTIES
	sorted_instances = {}
	unsorted_instances = {}
# -----------------


# PUBLIC METHODS
	def add_component (self, component: Component) -> Component:
		if component:
			if (not self.get_component(type(component)) and component.once) or not component.once:
				self.components.append(component)
				self.components[-1].game_object = self
				component.game_object = self
				return component
		print(str(type(component)) + " already attached to " + self.name)

	def get_component (self, type_name: T) -> Component:
		for c in self.components:
			if str(c.__class__) == str(type_name): return c

	def get_components (self, type_name: T) -> list:
		components: list[Component] = []
		for c in self.components:
			if str(c.__class__) == str(type_name): components.append(c)
		return components
# --------------