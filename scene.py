from components import *

class Scene (): # ------------------------ add get scene objects function
	def __init__ (self, name):
		self.name = name

	def print_global_tree (self):
		print(f"+ GLOBAL TRANSFORM TREE (SCENE: {self.name}) +")
		for transform in list(Transform.instances.values()):
			if not transform.parent and transform.game_object.scene == self: transform.print_local_tree(0)
		print("+ --------------------- +")

	scenes = {}
	active_scene = None