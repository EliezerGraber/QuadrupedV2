import math
from UI import UI
from itertools import combinations, permutations
import numpy as np
import functools
from utils import *

class Robot():

	def __init__(self, ui, center, leg_dist, leg_length, balance_safety):
		self.ui = ui
		self.ui.bind_movement(self.move)
		self.center = {"pos": center, "color": "white"}
		self.leg_dist = leg_dist
		self.leg_length = leg_length
		self.leg_anchors = [
						{
							"pos": center + np.array([leg_dist/math.sqrt(2), -leg_dist/math.sqrt(2)]), "color": "yellow"
						},
						{
							"pos": center + np.array([leg_dist/math.sqrt(2), leg_dist/math.sqrt(2)]), "color": "blue"
						},
						{
							"pos": center + np.array([-leg_dist/math.sqrt(2), -leg_dist/math.sqrt(2)]), "color": "red"
						},
						{
							"pos": center + np.array([-leg_dist/math.sqrt(2), leg_dist/math.sqrt(2)]), "color": "green"
						},
					]
		self.legs = self.leg_anchors
		self.free_leg = 0;
		self.balance_safety = balance_safety

	def draw(self):
		self.balance_check()
		for leg in self.legs:
			self.ui.draw_point(leg["pos"], 5, leg["color"])
		self.ui.draw_point(self.center["pos"], 5, self.center["color"])

	def balance_check(self):
		triangles = combinations([0, 1, 2, 3], 3)
		viable_tris = []
		for triangle in triangles:
			if is_point_in_triangle(self.legs[triangle[0]]["pos"], self.legs[triangle[1]]["pos"], self.legs[triangle[2]]["pos"], self.center["pos"]):
				self.ui.draw_triangle(self.legs[triangle[0]]["pos"], self.legs[triangle[1]]["pos"], self.legs[triangle[2]]["pos"], self.legs[triangle[2]]["color"])
				viable_tris.append(triangle)
		return viable_tris

	def find_free_legs(self, viable_tris):
		#viable_tris = balance_check
		if(len(viable_tris) == 1):
			return viable_tris[0] #return triangle or free leg?
		elif(len(viable_tris) == 2):
			return #both free leg options
		elif(len(viable_tris) == 0):
			return #all legs as free
		else:
			print("?")
			return None

	def find_target_leg(self, direction_v, triangle):
		side = find_side_of_triangle(self.legs, triangle, direction_v)
		#if np.dot(self.legs[side[0]] - self.legs[side[1]], direction_v) > 0
		#???

	def move(self, direction):
		direction_v = np.array([int(direction == "Right") - int(direction == "Left"), int(direction == "Up") - int(direction == "Down")])
		norm = np.linalg.norm(direction_v)
		direction_u = direction_v/norm
		self.center["pos"] = self.center["pos"] + direction_v


#locate free leg (there might be two)
#check if free leg is replacing or moving
#if moving - move to create ideal triangle
#locate target leg (leg that vector of movement points through active triangle)
#pick between two free legs (closer to target)
#log free leg that isn't being used
#replace, make target leg free






###	def move_free_leg(self, direction_v, next_leg, alternate leg):
		"""rotate_angle = (direction + 45) % 90 - 45
		axis = round(direction / 90) * 90 % 360

		if(np.dpt(self.legs[self.free_leg] - self.center, direction_u) > 0):
			self.legs[self.free_leg] = direction_v + self.leg_anchors[self.free_leg] #u * self.leg_dist + self.leg_anchors[self.free_leg]
		else:
			if(self.free_leg % 3 == 0):
				(self.legs[1] + self.legs[2]) / 2
			self.legs[self.free_leg] = """

		#determine if free leg is moving or replacing
			#is it behind center or in front (which side of line perpendicular to direction vector at center)
		#update location
			#if moving, move direction vector as far as bounds permit
			#if replacing, move towards line between adjacent legs, proportion equal to roate_angle/45, no further than past center plus safety
		#set new free leg

		#code for recentering body twist and gait along new forward

		#first version - no switching directions mid leg movement. later, allow for continous control

	#need function for rotating body without moving leg or center positions

#ALGO pseudocode

#walk orders:
#1302 - left
#0123 - straight

#legs:
#31
#20

#midstep position and full step positions
#switch axis (90 degrees) after midstep, use original leg order. switch after full step, use new leg order. switch direction, reverse leg order
#rotate (45 degrees or less) - pick a leg to rotate from. move other three, starting from the back leg. back to middle, middle to front, front forward in new direction
#combine switch axis and rotate for 45 to 135 either direction. combine switch direction for 135 to 180 either direction

#at some point try to twist body based on leg position in order to face the right direction

#algo is based on leg replacement principle. replace one leg with the next in order to free the front leg. order of replacement depends on direction
#amount of rotation drives which of the two adjacent legs the free leg moves closest to
#straight is replace, move, replace, move. rotate is replace, replace, move. in order to shift the center, the algo must try to predict which leg will be free next