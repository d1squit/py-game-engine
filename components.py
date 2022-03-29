from vector2 import *


class Component ():
	def __init__ (self, once=True):
		self.gameObject = None
		self.once = once
	
	def component_update (): print("Empty Component")


class Transform (Component):
	def __init__ (self, position=Vector2(), rotation=0, scale=Vector2(), once=True, use_meta=False):
		super().__init__(once)
		self.once = once
		self.use_meta = use_meta

		if self.use_meta: Transform.instances[id(self)] = self

		self.__position: Vector2 = position
		self.__rotation: float = rotation
		self.__scale: Vector2 = scale

		self.__local_position: Vector2 = Vector2()
		self.__local_rotation: float = 0
		self.__local_scale: Vector2 = Vector2()

		self.__childs: list[Transform] = []
		self.parent: Transform = None
		self.root: Transform = None

		self.component_update()


# OPERATORS
	def __repr__ (self):
		return f"Transform (Position: {self.__position}, Rotation: {self.__rotation}, Scale: {self.__scale})"

	def __str__ (self):
		return f"Transform (Position: {self.__position}, Rotation: {self.__rotation}, Scale: {self.__scale})"

	def __del__ (self):
		if self.use_meta: Transform.instances.pop(id(self))
	
	def __add__ (self, other):
		return Transform(self.__position + other.__position, self.__rotation + other.__rotation, self.__scale + other.__scale)
# ---------


# PUBLIC METHODS
	def childs_update (self, delta):
		for tr in Transform.instances.values():
			if tr in self.__childs:
				tr.gameObject.transform += delta
				tr.childs_update(Transform())

	def transforms_update (self):
		if (self.parent):
			self.__position = self.__local_position + self.parent.position
			self.__rotation = self.__local_rotation + self.parent.rotation
			self.__scale = self.__local_scale + self.parent.scale

	def local_transforms_update (self):
		if (self.parent):
			self.__local_position = self.__position - self.parent.position
			self.__local_rotation = self.__rotation - self.parent.rotation
			self.__local_scale = self.__scale - self.parent.scale

	def component_update (self):
		if not self.parent: self.root = self
		for child in self.__childs: child.parent = self

		if self.root:
			for child in self.__childs: child.root = self.root

		self.local_transforms_update()
		self.transforms_update()

	def attach_to (self, parent):
		parent.__childs.append(self)
		self.parent = parent
		self.local_transforms_update()

	# def detach (self):
	# 	self.parent.__childs.remove(self)
	# 	self.parent = None
	# 	self.local_transforms_update()

	def print_local_tree (self, iter):
		string = ""
		for i in range(iter): string += "--"
		print(string + "> " + self.gameObject.name)
		iter += 1
		for child in self.__childs: child.print_local_tree(iter)
# --------------


# PROPERTIES
	@property
	def childs (self):
		result = Transform.get_instances()
		for tr in result:
			if not tr in self.__childs:
				result.remove(tr)
		return result


	@property
	def position (self) -> Vector2:
		return self.__position
	@position.setter
	def position (self, pos: Vector2):
		self.childs_update(Transform(position=pos - self.__position))
		self.__position = pos
		self.local_transforms_update()
		self.component_update()
	
	@property
	def rotation (self) -> float:
		return self.__rotation
	@rotation.setter
	def rotation (self, rot: float):
		self.childs_update(Transform(rotation=rot - self.__rotation))
		self.__rotation = rot
		self.local_transforms_update()
		self.component_update()
	
	@property
	def scale (self) -> Vector2:
		return self.__scale
	@scale.setter
	def scale (self, scale: Vector2):
		self.childs_update(Transform(scale=scale - self.__scale))
		self.__scale = scale
		self.local_transforms_update()
		self.component_update()

	
	@property
	def local_position (self) -> Vector2:
		return self.__local_position
	@local_position.setter
	def local_position (self, local_pos: Vector2):
		self.childs_update(Transform(position=local_pos - self.__local_position))
		self.__local_position = local_pos
		self.transforms_update()
		self.component_update()
	
	@property
	def local_rotation (self) -> float:
		return self.__local_rotation
	@local_rotation.setter
	def local_rotation (self, local_rot: float):
		self.childs_update(Transform(rotation=local_rot - self.__local_rotation))
		self.__local_rotation = local_rot
		self.transforms_update()
		self.component_update()
	
	@property
	def local_scale (self) -> Vector2:
		return self.__local_scale
	@local_scale.setter
	def local_scale (self, local_scale: Vector2):
		self.childs_update(Transform(scale=local_scale - self.__local_scale))
		self.__local_scale = local_scale
		self.transforms_update()
		self.component_update()
# ----------


# STATIC PROPERTIES
	instances = {}
# -----------------