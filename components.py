from sprite import *
import pygame
import math


class Component ():
	def __init__ (self, once=True):
		self.once: bool = once
		self.cached = False
		
		self.__game_object = None

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
	def start (self): pass
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

	@property
	def transform (self):
		return self.__game_object.get_component(Transform)
	@transform.setter
	def transform (self, tr):
		self.__game_object.get_component(Transform).position = tr.position
		self.__game_object.get_component(Transform).rotation = tr.rotation
		self.__game_object.get_component(Transform).scale = tr.scale
# ----------


class SpriteRenderer (Component):
	def __init__ (self, sprite: Sprite, center=False, once=True):
		super().__init__(once)
		self.sprite = sprite
		self.center = center


# OPERATORS
	def __repr__ (self):
		return f"Sprite (Sprite: {self.sprite})"

	def __str__ (self):
		return f"Sprite (Sprite: {self.sprite})"
# ---------


# OVERRIDED METHODS
	def rot_center(self, image, angle, x, y):
		rotated_image = pygame.transform.rotate(image, angle)
		if self.center:
			new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
			return rotated_image, new_rect
		else: return rotated_image, image.get_rect()

	def update (self, args):
		if self.sprite.texture:
			texture = self.sprite.texture
			texture = transform.scale(texture, (texture.get_size()[0] * self.transform.scale.x, texture.get_size()[1] * self.transform.scale.y))
			rotated_texture, pos = self.rot_center(texture, self.transform.rotation, self.transform.position.x, self.transform.position.y)
			
			args['SceneManager'].window.blit(rotated_texture, pos)
# -----------------


# STATIC PROPERTIES
	instances = {}
# -----------------


class Transform (Component):
	def __init__ (self, position=Vector2(), rotation=0, scale=Vector2(1, 1), once=True):
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

	# div mul sub operators ------------------------------------
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
		angle = math.degrees(math.atan2(target.y - self.position.y, target.x - self.position.x))
		self.rotation = -angle - 90
		return angle

	def rotate_around (self, axis: Vector2, angle: float) -> Vector2:
		vector = Vector2.angle_vector(self.position - axis, angle)
		self.position = vector + axis
		return vector + axis
# --------------


# PROPERTIES
	@property
	def down (self):
		return Transform(-self.up.position, self.__rotation, self.__scale)
	
	@property
	def left (self):
		return Transform(-self.right.position, self.__rotation, self.__scale)
	
	@property
	def right (self):
		return Transform(Vector2.angle_vector(Vector2.right(), -self.__rotation), self.__rotation, self.__scale)

	@property
	def up (self):
		return Transform(-Vector2.angle_vector(Vector2.up(), -self.__rotation), self.__rotation, self.__scale)

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

	# local pos setter dont move object
	@property
	def local_position (self) -> Vector2:
		return self.__local_position
	@local_position.setter
	def local_position (self, local_pos: Vector2):
		self.childs_update(Transform(position=local_pos - self.__local_position))
		self.__local_position = local_pos
	
	@property
	def local_rotation (self) -> float:
		return self.__local_rotation
	@local_rotation.setter
	def local_rotation (self, local_rot: float):
		self.childs_update(Transform(rotation=local_rot - self.__local_rotation))
		self.__local_rotation = local_rot
	
	@property
	def local_scale (self) -> Vector2:
		return self.__local_scale
	@local_scale.setter
	def local_scale (self, local_scale: Vector2):
		self.childs_update(Transform(scale=local_scale - self.__local_scale))
		self.__local_scale = local_scale
# ----------


# STATIC PROPERTIES
	instances = {}
# -----------------