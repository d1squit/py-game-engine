from vector2 import *
from pygame import key, mouse, K_d, K_a, K_w, K_s

class Input ():
	@staticmethod
	def mouse_position (): return Vector2(mouse.get_pos()[0], mouse.get_pos()[1])

	def get_axis (axis_key: str):
		for idx, state in enumerate(list(Input.axis[axis_key].keys())):
			if state != "default":
				if eval(state): return list(Input.axis[axis_key].values())[idx]
			else: return Input.axis[axis_key]["default"]

	axis = {
		"Horizontal": {"key.get_pressed()[K_d]": 1, "key.get_pressed()[K_a]": -1, "default": 0},
		"Vertical": {"key.get_pressed()[K_w]": 1, "key.get_pressed()[K_s]": -1, "default": 0}
	}

