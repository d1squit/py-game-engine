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
		return Vector2.ClampMagnitude(self, 1)
# --------------


# STATIC METHODS
	@staticmethod
	def Angle (from_vector, to_vector):
		distance = Vector2.Distance(from_vector, to_vector)
		a_side = from_vector.magnitude
		b_side = to_vector.magnitude
		cos = abs((a_side ** 2 + b_side ** 2 - distance ** 2) / (-2 * a_side * b_side)) # cos theorem =>
		return math.acos(cos)

	@staticmethod
	def ClampMagnitude (vector, maxLength: float):
		yx_factor = vector.y / vector.x
		return maxLength / (1 + yx_factor) ** 0.5

	@staticmethod
	def Dot (lhs, rhs):
		distance = Vector2.Distance(lhs, rhs)
		a_side = lhs.magnitude
		b_side = rhs.magnitude
		cos = abs((a_side ** 2 + b_side ** 2 - distance ** 2) / (-2 * a_side * b_side)) # cos theorem =>
		return a_side * b_side * cos

	@staticmethod
	def Distance (a, b):
		return ((b.x - a.x) ** 2 + (b.y - a.y) ** 2) ** 0.5

	@staticmethod
	def Max (lhs, rhs):
		return Vector2(max([lhs.x, rhs.x]), max([lhs.y, rhs.y]))
	
	@staticmethod
	def Min (lhs, rhs):
		return Vector2(min([lhs.x, rhs.x]), min([lhs.y, rhs.y]))

	@staticmethod
	def AngleVector (vector, angle: float): # -degrees
		angle = math.radians(angle)
		return Vector2(round(vector.x * math.cos(angle) - vector.y * math.sin(angle), 9),
					   round(vector.x * math.sin(angle) + vector.y * math.cos(angle), 9))

	@staticmethod
	def Reflect (inDirection, inNormal):
		normal_angle = Vector2.SignedAngle(inDirection, inNormal)
		return Vector2.AngleVector(inDirection, 2 * normal_angle)

	@staticmethod
	def Scale (a, b):
		return Vector2(a.x * b.x, a.y * b.y)

	@staticmethod
	def SignedAngle (from_vector, to_vector):
		distance = Vector2.Distance(from_vector, to_vector)
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

		# -shorthand inits
	@property
	def zero (): return Vector2(0, 0)

	@property
	def one (): return Vector2(1, 1)

	@property
	def down (): return Vector2(0, -1)

	@property
	def left (): return Vector2(-1, 0)

	@property
	def right (): return Vector2(1, 0)

	@property
	def up (): return Vector2(0, 1)
		# -
# ----------