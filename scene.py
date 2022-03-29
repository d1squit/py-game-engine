from components import *
from gameobject import GameObject

class Scene ():
	def __init__ (self): pass

	def print_global_tree (self):
		for transform in list(Transform.instances.values()):
			if not transform.parent: transform.print_local_tree(0)