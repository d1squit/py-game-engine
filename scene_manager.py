from scene import *

class SceneManager ():

# STATIC METHODS
	@staticmethod
	def create_scene (scene_name: str, active=True):
		SceneManager.scenes[scene_name] = Scene(scene_name)
		if active: SceneManager.active_scene = SceneManager.scenes[scene_name]
		return SceneManager.scenes[scene_name]
# --------------


# STATIC PROPERTIES
	scenes = {}
	active_scene = None
# -----------------