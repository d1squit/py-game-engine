from components import *
from typing import TypeVar, Generic

T = TypeVar('T')


class GameObject (Generic[T]):
	def __init__ (self, name: str, tag="", layer=[]):
		self.name = name
		self.tag = tag
		self.layer = layer

		self.components: list[Component] = []
		self.add_component(Transform(use_meta=True))


# OPERATORS
	def __repr__ (self):
		return f"GameObject (Name: {self.name}, {self.transform})"

	def __str__ (self):
		return f"GameObject (Name: {self.name}, {self.transform})"
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


# PUBLIC METHODS
	def add_component (self, component: Component) -> Component:
		if component:
			if (not self.get_component(type(component)) and component.once) or not component.once:
				component.use_meta = True
				self.components.append(component)
				self.components[-1].game_object = self
				component.game_object = self
				return component
		print(str(type(component)) + " already attached to " + self.name)

	def get_component (self, type: T) -> Component:
		for c in self.components:
			if str(type(c)).__class__.__name__ == str(type(T)).__class__.__name__: return c

	def get_components (self, type: T) -> list:
		components: list[Component] = []
		for c in self.components:
			if type(c) == type(T): components.append(c)
		return components
# --------------