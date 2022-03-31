from sprite import *


class Component ():
	def __init__ (self, once=True):
		self.once: bool = once
		self.cached = False

		try: type(self).instances
		except AttributeError: type(self).instances = {}


# OPERATORS
	def __del__ (self):
		if self.cached: type(self).instances.pop(id(self))
	
	def cache (self):
		if not self.cached:
			type(self).instances[id(self)] = self
			self.cached = True
# ---------


# METHODS FOR OVERRIDING
	def update (self, args): pass
# ----------------------


# PROPERTIES
	@property
	def game_object (self):
		return self.__game_object
	@game_object.setter
	def game_object (self, object):
		self.name = object.name
		self.tag = object.tag
		self.__game_object = object
# ----------


class SpriteRenderer (Component):
	def __init__ (self, sprite: Sprite, once=True):
		super().__init__(once)
		self.sprite = sprite


# OPERATORS
	def __repr__ (self):
		return f"Sprite (Sprite: {self.sprite})"

	def __str__ (self):
		return f"Sprite (Sprite: {self.sprite})"
# ---------


# OVERRIDED METHODS
	def update (self, args):
		args['SceneManager'].window.blit(self.sprite.texture, (self.game_object.transform.position.x, self.game_object.transform.position.y))
# -----------------


# STATIC PROPERTIES
	instances = {}
# -----------------


class Transform (Component):
	def __init__ (self, position=Vector2(), rotation=0, scale=Vector2(), once=True):
		super().__init__(once)

		self.__position: Vector2 = position
		self.__rotation: float = rotation
		self.__scale: Vector2 = scale

		self.__local_position: Vector2 = Vector2()
		self.__local_rotation: float = 0
		self.__local_scale: Vector2 = Vector2()

		self.parent: Transform = None
		self.root: Transform = self

		self.name = ""
		self.tag = ""


# OPERATORS
	def __repr__ (self):
		return f"Transform (Position: {self.position}, Rotation: {self.rotation}, Scale: {self.scale})"

	def __str__ (self):
		return f"Transform (Position: {self.position}, Rotation: {self.rotation}, Scale: {self.scale})"
	
	def __add__ (self, other):
		return Transform(self.position + other.position, self.rotation + other.rotation, self.scale + other.scale)
# ---------


# PUBLIC METHODS
	def local_transforms_update (self):
		if (self.parent):
			self.__local_position = self.__position - self.parent.position
			self.__local_rotation = self.__rotation - self.parent.rotation
			self.__local_scale = self.__scale - self.parent.scale


	# --child indexes system

	def get_childs_indexes (self):
		indexes: list[int] = []
		for idx, tr in enumerate(list(Transform.instances.values())):
			if tr.parent == self: indexes.append(idx)
		return indexes

	def get_childs_index (self, index: int):
		return self.get_childs_indexes()[index]

	def find_child_index (self, name: str):
		for child in self.get_childs_indexes():
			if list(Transform.instances.values())[child].game_object.name == name: return child

	def childs_update (self, delta):
		for child in self.get_childs_indexes():
			if child in self.get_childs_indexes():
				list(Transform.instances.values())[child].game_object.transform += delta
				list(Transform.instances.values())[child].childs_update(Transform())

	def attach_to (self, parent):
		if self.game_object.scene == parent.game_object.scene:
			self.root = parent.root
			self.parent = parent
			self.local_transforms_update()
		else: raise Exception('The specified object to attach does not exist in this scene')

	def detach (self):
		self.parent = None
		self.local_transforms_update()

	def print_local_tree (self, iter):
		string = ""
		for i in range(iter): string += "--"
		print("| " + string + "> " + self.game_object.name)
		iter += 1
		for child in self.get_childs_indexes(): list(Transform.instances.values())[child].print_local_tree(iter)

	# --

	def look_at (self, target) -> float:
		angle = math.degrees(math.atan2(target.position.y - self.position.y, target.position.x - self.position.x))
		self.rotation += angle
		return angle

	def rotate_around (self, axis: Vector2, angle: float) -> Vector2:
		vector = Vector2.angle_vector(self.position - axis, angle)
		self.position = vector + axis
		return vector + axis
# --------------


# PROPERTIES
	@property
	def down (self):
		return Vector2.angle_vector(Vector2.down(), self.rotation)
	
	@property
	def left (self):
		return Vector2.angle_vector(Vector2.left(), self.rotation)
	
	@property
	def right (self):
		return Vector2.angle_vector(Vector2.right(), self.rotation)

	@property
	def up (self):
		return Vector2.angle_vector(Vector2.up(), self.rotation)

	@property
	def child_count (self) -> int:
		counter = 0
		for tr in list(Transform.instances.values()):
			if tr.parent == self: counter += 1
		return counter


	@property
	def position (self) -> Vector2:
		return self.__position
	@position.setter
	def position (self, pos: Vector2):
		self.childs_update(Transform(position=pos - self.__position))
		self.__position = pos
	
	@property
	def rotation (self) -> float:
		return self.__rotation
	@rotation.setter
	def rotation (self, rot: float):
		self.childs_update(Transform(rotation=rot - self.__rotation))
		self.__rotation = rot
	
	@property
	def scale (self) -> Vector2:
		return self.__scale
	@scale.setter
	def scale (self, scale: Vector2):
		self.childs_update(Transform(scale=scale - self.__scale))
		self.__scale = scale

	
	@property
	def local_position (self) -> Vector2:
		return self.__local_position
	@local_position.setter
	def local_position (self, local_pos: Vector2):
		self.__local_position = local_pos
	
	@property
	def local_rotation (self) -> float:
		return self.__local_rotation
	@local_rotation.setter
	def local_rotation (self, local_rot: float):
		self.__local_rotation = local_rot
	
	@property
	def local_scale (self) -> Vector2:
		return self.__local_scale
	@local_scale.setter
	def local_scale (self, local_scale: Vector2):
		self.__local_scale = local_scale
# ----------


# STATIC PROPERTIES
	instances = {}
# -----------------