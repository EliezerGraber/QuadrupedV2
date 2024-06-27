import math
from UI import UI
from itertools import combinations
import numpy as np

class Robot():

	def __init__(self, ui, center, leg_dist, leg_length):
		self.ui = ui
		self.ui.bind_movement(self.move)
		self.center = {"pos": center, "color": "white"}
		self.leg_dist = leg_dist
		self.leg_length = leg_length
		self.legs = [
						{
							"pos": center + np.array([leg_dist/math.sqrt(2), leg_dist/math.sqrt(2)]), "color": "yellow"
						},
						{
							"pos": center + np.array([leg_dist/math.sqrt(2), -leg_dist/math.sqrt(2)]), "color": "blue"
						},
						{
							"pos": center + np.array([-leg_dist/math.sqrt(2), -leg_dist/math.sqrt(2)]), "color": "red"
						},
						{
							"pos": center + np.array([-leg_dist/math.sqrt(2), 2*leg_dist/math.sqrt(2)]), "color": "green"
						},
					]

	def draw(self):
		self.balance_check()
		for leg in self.legs:
			self.ui.draw_point(leg["pos"], 5, leg["color"])
		self.ui.draw_point(self.center["pos"], 5, self.center["color"])


	def balance_check(self):
		triangles = combinations(self.legs, 3)
		for triangle in triangles:
			if self.is_point_in_triangle(triangle[0]["pos"], triangle[1]["pos"], triangle[2]["pos"], self.center["pos"]):
				self.ui.draw_triangle(triangle[0]["pos"], triangle[1]["pos"], triangle[2]["pos"], triangle[2]["color"])

	"""Returns the orientation of the ordered triplet (p, q, r).
		0 -> p, q and r are collinear
		1 -> Clockwise
		-1 -> Counterclockwise"""
	def orientation(self, p, q, r):
		val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
		return int(math.copysign(1, val)) if val != 0 else 0

	def is_point_in_triangle(self, p, q, r, point):
		o1 = self.orientation(p, q, point)
		o2 = self.orientation(q, r, point)
		o3 = self.orientation(r, p, point)
		return (o1 == o2 == o3) #or o1 == 0 or o2 == 0 or o3 == 0

	def move(self, direction):
		vector = np.array([int(direction == "Right") - int(direction == "Left"), int(direction == "Up") - int(direction == "Down")])
		self.center["pos"] = self.center["pos"] + vector