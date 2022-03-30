from components import *

class Scene ():
	def __init__ (self, name):
		self.name = name

	def print_global_tree (self):
		print(f"+ GLOBAL TRANSFORM TREE (SCENE: {self.name}) +")
		for transform in list(Transform.instances.values()):
			if not transform.parent: transform.print_local_tree(0)
		print("+ --------------------- +")