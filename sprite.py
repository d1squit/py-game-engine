from vector2 import *
from pygame import transform, image

class Sprite ():
	def __init__ (self, texture_path: str = "", size: Vector2 = Vector2()):
		self.__size = size
		self.__texture_path = texture_path
		self.texture = None

		self.load_texture()

	@property
	def texture_path (self):
		return self.__texture_path
	@texture_path.setter
	def texture_path (self, path: str):
		self.__texture_path = path
		self.load_texture()

	@property
	def size (self):
		return self.__size
	@size.setter
	def size (self, size: Vector2):
		self.__size = size
		self.load_texture()

	def load_texture (self):
		if self.__texture_path != "":
			if self.size == Vector2():
				self.texture = image.load(self.texture_path)
				self.size = Vector2(self.texture.get_size()[0], self.texture.get_size()[1])
			else: self.texture = transform.scale(image.load(self.texture_path), (round(self.size.x), round(self.size.y)))