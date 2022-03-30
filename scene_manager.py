import sys
from gameobject import *
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

			SceneManager.window.fill(SceneManager.screen_color)
			SceneManager.main_cycle()

			pygame.display.update()
			SceneManager.fps_clock.tick(SceneManager.fps)

	
	@staticmethod
	def main_cycle ():
		for game_object in list(GameObject.instances.values()):
			if game_object.scene == Scene.active_scene:
				for component in game_object.components: component.update({'SceneManager': SceneManager})


	@staticmethod
	def create_scene (scene_name: str, active=True):
		Scene.scenes[scene_name] = Scene(scene_name)
		if active: Scene.active_scene = Scene.scenes[scene_name]
		return Scene.scenes[scene_name]
# --------------


# STATIC PROPERTIES
	window: pygame.Surface
	fps_clock: pygame.time.Clock

	fps = 60
	screen_width = 1120
	screen_height = 630
	screen_color = (255, 255, 255)
	fullscreen = False

	caption = "PyGameEngineProject"
# -----------------