import math

class Vector2 ():
	def __init__ (self, x=0, y=0):
		self.x = x
		self.y = y

# OPERATORS
	def __repr__ (self):
		return f"Vector2({self.x}, {self.y})"

	def __str__ (self):
		return f"Vector2({self.x}, {self.y})"

	def __eq__ (self, other):
		return self.x == other.x and self.y == other.y
	
	def __add__ (self, other):
		if (type(other) == Vector2): return Vector2(self.x + other.x, self.y + other.y)
		elif (type(other) == int or type(other) == float): return Vector2(self.x + other, self.y + other)

	def __sub__ (self, other):
		if (type(other) == Vector2): return Vector2(self.x - other.x, self.y - other.y)
		elif (type(other) == int or type(other) == float): return Vector2(self.x - other, self.y - other)

	def __mul__ (self, other):
		if (type(other) == Vector2): return Vector2(self.x * other.x, self.y * other.y)
		elif (type(other) == int or type(other) == float): return Vector2(self.x * other, self.y * other)

	def __truediv__ (self, other):
		if (type(other) == Vector2): return Vector2(self.x / other.x, self.y / other.y)
		elif (type(other) == int or type(other) == float): return Vector2(self.x / other, self.y / other)
# ---------


# PUBLIC METHODS
	def Set (self, _x, _y):
		self.x = _x
		self.y = _y
	
	def Normalize (self): # sqrt(x^2 + f*y^2) = 1, f - factor
		return Vector2.clamp_magnitude(self, 1)
# --------------


# STATIC METHODS
	@staticmethod
	def angle (from_vector, to_vector) -> float:
		distance = Vector2.distance(from_vector, to_vector)
		a_side = from_vector.magnitude
		b_side = to_vector.magnitude
		cos = abs((a_side ** 2 + b_side ** 2 - distance ** 2) / (-2 * a_side * b_side)) # cos theorem =>
		return math.acos(cos)

	@staticmethod
	def angle_vector (vector, angle: float): # -degrees
		angle = math.radians(angle)
		return Vector2(round(vector.x * math.cos(angle) - vector.y * math.sin(angle), 9),
					   round(vector.x * math.sin(angle) + vector.y * math.cos(angle), 9))

	@staticmethod
	def clamp_magnitude (vector, maxLength: float) -> float:
		yx_factor = vector.y / vector.x
		return maxLength / (1 + yx_factor) ** 0.5

	@staticmethod
	def dot (lhs, rhs) -> float:
		return lhs.x * rhs.x + lhs.y * rhs.y

	@staticmethod
	def distance (a, b) -> float:
		return ((b.x - a.x) ** 2 + (b.y - a.y) ** 2) ** 0.5

	@staticmethod
	def max (lhs, rhs):
		return Vector2(max([lhs.x, rhs.x]), max([lhs.y, rhs.y]))
	
	@staticmethod
	def min (lhs, rhs):
		return Vector2(min([lhs.x, rhs.x]), min([lhs.y, rhs.y]))

	@staticmethod
	def reflect (inDirection, inNormal):
		normal_angle = Vector2.signed_angle(inDirection, inNormal)
		return Vector2.angle_vector(inDirection, 2 * normal_angle)

	@staticmethod
	def scale (a, b):
		return Vector2(a.x * b.x, a.y * b.y)

	@staticmethod
	def signed_angle (from_vector, to_vector) -> float:
		distance = Vector2.distance(from_vector, to_vector)
		a_side = from_vector.magnitude
		b_side = to_vector.magnitude
		cos = abs((a_side ** 2 + b_side ** 2 - distance ** 2) / (-2 * a_side * b_side)) # cos theorem =>
		return math.degrees(math.acos(cos))
# --------------


# PROPERTIES
	@property
	def magnitude (self): return (self.x ** 2 + self.y ** 2) ** 0.5

	@property
	def normilized (self): return self.Normalize()

	# --shorthand inits
	@staticmethod
	def zero (): return Vector2(0, 0)

	@staticmethod
	def one (): return Vector2(1, 1)
	
	@staticmethod
	def down (): return Vector2(0, -1)

	@staticmethod
	def left (): return Vector2(-1, 0)

	@staticmethod
	def right (): return Vector2(1, 0)

	@staticmethod
	def up (): return Vector2(0, 1)
	# --
# ----------