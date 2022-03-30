from vector2 import *
import pygame

class Sprite ():
	def __init__ (self, texture_path: str, size: Vector2 = Vector2()):
		if size == Vector2(): self.texture = pygame.image.load(texture_path)
		else: self.texture = pygame.transform.scale(pygame.image.load(texture_path), (size.x, size.y))

		self.size = size