import math
from itertools import combinations, permutations

def line_intersection(A, B, P, v):
	AB = B.sub(A)
	AP = P.sub(A)

	#A + tAB = P + sV //lines are set equal
	#t = (AP + sV)/AB, s = (tAB - AP)/V
	#cross to eliminate s and t
	#t = APxV/ABxV, s = -APxAB/VxAB = APxAB/ABxV

	denom = AB.cross(v)

	# Check if the lines are parallel (cross is zero)
	if denom == 0:
		return False, 0

	t = AP.cross(v) / denom
	s = AP.cross(AB) / denom

	# Check if the intersection is within the line segment and vector direction
	if 0 <= t < 1 and s > 0:
		return True, s
	else:
		return False, s

#takes array points and indices of three points
def find_side_of_triangle(points, tri, direction_v, center):
	sides = combinations(tri, 2)
	#sides = [(A, B), (B, C), (C, A)]
	for side in sides:
		intersection, s = line_intersection(points[side[0]]["pos"], points[side[1]]["pos"], center, direction_v)
		if intersection:
			return side
	return None

"""Returns the orientation of the ordered triplet (p, q, r).
	0 -> p, q and r are collinear
	1 -> Clockwise
	-1 -> Counterclockwise"""
def orientation(p, q, r):
	val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
	return int(math.copysign(1, val)) if val != 0 else 0

def is_point_in_triangle(p, q, r, point):
	o1 = orientation(p, q, point)
	o2 = orientation(q, r, point)
	o3 = orientation(r, p, point)
	return (o1 == o2 == o3) or o1 == 0 or o2 == 0 or o3 == 0

def unit_vector(vector):
    return vector.div(vector.magnitude())

def angle_between(v1, v2):
    #v1_u = unit_vector(v1)
    #v2_u = unit_vector(v2)
    #return math.acos(np.clip(v1_u.dot(v2_u), -1.0, 1.0))
    angle = math.atan2(v2.y, v2.x) - math.atan2(v1.y, v1.x)
    if angle > math.pi:
    	angle -= 2 * math.pi
    elif angle <= -math.pi:
    	angle += 2 * math.pi
    return angle

def triangle_equality(points):
    a, b, c = points
    sides = [b.sub(a).magnitude(), c.sub(b).magnitude(), a.sub(c).magnitude()]
    std_dev = std(sides)
    return std_dev

def closest_to_equilateral(legs, tris):
	min_std_dev = float('inf')
	closest_set = None

	for i, tri in enumerate(tris):
		std_dev = triangle_equality([legs[tri[0]]["pos"], legs[tri[1]]["pos"], legs[tri[2]]["pos"]])
		if std_dev < min_std_dev:
			min_std_dev = std_dev
			closest_set = i

	return closest_set

def farthest_vector(target, vector_list):
    distances = [target.sub(v).magnitude() for v in vector_list]
    closest_index = argmax(distances)
    return closest_index

def centroid_legs(legs, tri):
	return centroid_tri(legs[tri[0]]["pos"], legs[tri[1]]["pos"], legs[tri[2]]["pos"])

def centroid_tri(a, b, c): #triangle class?
	Gx = (a.x + b.x + c.x) / (3)
	Gy = (a.y + b.y + c.y) / (3)
	return vector2(Gx, Gy)

def centroid_quad(a, b, c, d):
	#centroid of a quad is area weighted average of the centroids of opposite triangles. however, since we don't know which triangles are opposites, we will area average all 4 possible triangles 
	c_tris = [centroid_tri(tri[0], tri[1], tri[2]).mult(tri_area(tri)) for tri in combinations([a, b, c, d], 3)]
	total_area = sum([tri_area(tri) for tri in combinations([a, b, c, d], 3)])
	Gx = sum(tri.x for tri in c_tris) / total_area
	Gy = sum(tri.y for tri in c_tris) / total_area
	return vector2(Gx, Gy)

def tri_area(points):
	a, b, c = points
	AB = b.sub(a)
	AC = c.sub(a)
	cross_product = AB.cross(AC)
	area = 0.5 * abs(cross_product)
	return area

class vector2():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def cross(self, v):
		return self.x * v.y - self.y * v.x

	def dot(self, v):
		return self.x * v.x + self.y * v.y

	def mult(self, s):
		return vector2(self.x * s, self.y * s)

	def div(self, s):
		return vector2(self.x / s, self.y / s)

	def magnitude(self):
		return math.sqrt(self.x**2 + self.y**2)

	def add(self, v):
		return vector2(self.x + v.x, self.y + v.y)

	def sub(self, v):
		return vector2(self.x - v.x, self.y - v.y)

def mean(data):
	return sum(data) / len(data)

def std(data):
	if len(data) == 0:
		raise ValueError("The data list cannot be empty")
	mu = mean(data)
	variance = sum((x - mu) ** 2 for x in data) / len(data)
	return math.sqrt(variance)

def argmax(data):
	if not data:
		raise ValueError("The input data list cannot be empty")
	max_index = 0
	max_value = data[0]
	for i, value in enumerate(data):
		if value > max_value:
			max_index = i
			max_value = value
	return max_index
