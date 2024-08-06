import math
from itertools import combinations, permutations
import numpy as np

def line_intersection(A, B, P, v):
	AB = B - A
	AP = P - A

	#A + tAB = P + sV //lines are set equal
	#t = (AP + sV)/AB, s = (tAB - AP)/V
	#cross to eliminate s and t
	#t = APxV/ABxV, s = -APxAB/VxAB = APxAB/ABxV

	denom = np.cross(AB, v)

	# Check if the lines are parallel (cross is zero)
	if denom == 0:
		return False

	t = np.cross(AP, v) / denom
	s = np.cross(AP, AB) / denom

	# Check if the intersection is within the line segment and vector direction
	if 0 <= t < 1 and s >= 0:
		return True
	else:
		return False

#takes array points and indices of three points
def find_side_of_triangle(points, tri, direction_v, center):
	sides = combinations(tri, 2)
	#sides = [(A, B), (B, C), (C, A)]
	for side in sides:
		intersection = line_intersection(points[side[0]]["pos"], points[side[1]]["pos"], center, direction_v)
		if intersection:
			return side
	return None

"""Returns the orientation of the ordered triplet (p, q, r).
	0 -> p, q and r are collinear
	1 -> Clockwise
	-1 -> Counterclockwise"""
def orientation(p, q, r):
	val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
	return int(math.copysign(1, val)) if val != 0 else 0

def is_point_in_triangle(p, q, r, point):
	o1 = orientation(p, q, point)
	o2 = orientation(q, r, point)
	o3 = orientation(r, p, point)
	return (o1 == o2 == o3) #or o1 == 0 or o2 == 0 or o3 == 0

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))