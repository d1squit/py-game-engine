import sys
from scene import *
from gameobject import GameObject
import pygame

class SceneManager ():

# STATIC METHODS
	@staticmethod
	def init_game ():
		pygame.init()
		pygame.display.set_caption(SceneManager.caption)

		if SceneManager.fullscreen: SceneManager.window = pygame.display.set_mode((SceneManager.screen_width, SceneManager.screen_height), pygame.FULLSCREEN)
		else: SceneManager.window = pygame.display.set_mode((SceneManager.screen_width, SceneManager.screen_height), pygame.RESIZABLE)

		SceneManager.fps_clock = pygame.time.Clock()

		while (True):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			SceneManager.main_cycle()

			pygame.display.update()
			SceneManager.fps_clock.tick(SceneManager.fps)

	@staticmethod
	def sort_gameobjects ():
		for game_object in list(GameObject.unsorted_instances.values()):
			game_object.scene = SceneManager.active_scene # --------------------- exception check !
			GameObject.sorted_instances[list(GameObject.unsorted_instances.keys())[0]] = game_object
			del GameObject.unsorted_instances[list(GameObject.unsorted_instances.keys())[0]]

	
	@staticmethod
	def main_cycle ():
		if not len(GameObject.unsorted_instances): SceneManager.sort_gameobjects()

		for game_object in list(GameObject.unsorted_instances.values()):
			for component in game_object.components: component.update({'SceneManager': SceneManager})


	@staticmethod
	def create_scene (scene_name: str, active=True):
		SceneManager.scenes[scene_name] = Scene(scene_name)
		if active: SceneManager.active_scene = SceneManager.scenes[scene_name]
		return SceneManager.scenes[scene_name]
# --------------


# STATIC PROPERTIES
	window: pygame.Surface
	fps_clock: pygame.time.Clock

	fps = 60
	screen_width = 1120
	screen_height = 630
	fullscreen = False

	pixels_per_unit = 64

	caption = "PyGameEngineProject"

	scenes = {}
	active_scene = None
# -----------------