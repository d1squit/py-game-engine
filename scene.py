from components import *

class Scene ():
	def __init__ (self, name: str):
		self.name = name

	def print_global_tree (self):
		print(f"+ GLOBAL TRANSFORM TREE (Scene: {self.name}) +")
		for transform in list(Transform.instances.values()):
			if not transform.parent and transform.game_object.scene == self: transform.print_local_tree(0)
		print("+ --------------------- +")