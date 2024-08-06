import math
from UI import UI
from itertools import combinations, permutations
import numpy as np
import functools
from utils import *
import time

class Robot():

	def __init__(self, ui, center, leg_dist, leg_length, balance_safety):
		self.ui = ui
		self.ui.bind_movement(self.move)
		self.center = {"pos": center, "color": "gray"}
		self.ideal_center = {"pos": center, "color": "white"}
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
		self.ui.draw_point(self.ideal_center["pos"], 5, self.ideal_center["color"])

	def balance_check(self):
		triangles = combinations([0, 1, 2, 3], 3)
		viable_tris = []
		for triangle in triangles:
			if is_point_in_triangle(self.legs[triangle[0]]["pos"], self.legs[triangle[1]]["pos"], self.legs[triangle[2]]["pos"], self.center["pos"]):
				self.ui.draw_triangle(self.legs[triangle[0]]["pos"], self.legs[triangle[1]]["pos"], self.legs[triangle[2]]["pos"], self.legs[triangle[2]]["color"])
				viable_tris.append(triangle)
		return viable_tris

	def find_free_legs(self, viable_tris):
		#viable_tris = self.balance_check()
		if(len(viable_tris) == 1):
			return [leg for leg in [0, 1, 2, 3] if leg not in viable_tris[0]]
			#return viable_tris[0] #return triangle or free leg?
		elif(len(viable_tris) == 2):
			return [leg for leg in [0, 1, 2, 3] if leg not in viable_tris[0] or leg not in viable_tris[1]]
		elif(len(viable_tris) == 0):
			return [0, 1, 2, 3]
		else:
			print("?")
			return None

	def find_target_leg(self, direction_v, triangle):
		side = find_side_of_triangle(self.legs, triangle, direction_v, self.center["pos"])
		if np.dot(self.legs[side[0]]["pos"] - self.legs[side[1]]["pos"], direction_v) > 0:
			return side[1]
		else:
			return side[0]

	def move(self, direction):
		direction_v = np.array([int(direction == "Right") - int(direction == "Left"), int(direction == "Up") - int(direction == "Down")])
		norm = np.linalg.norm(direction_v)
		direction_u = direction_v/norm
		self.ideal_center["pos"] = self.ideal_center["pos"] + direction_v #+=?
		self.center["pos"] = self.center["pos"] + direction_v #only update real center if moving wont disrupt the active triangle
		self.move_a_leg(direction_v)

	def are_legs_adjacent(self, l1, l2):
		return (l1 + l2) %3 == 1 or (l1 + l2) %3 == 2

	def get_leg_pairs(self, direction_v):
		tris = self.balance_check()
		free_legs = self.find_free_legs(tris)
		leg_pairs = [];
		for free_leg in free_legs:
			target_leg = self.find_target_leg(direction_v, (leg for leg in [0, 1, 2, 3] if leg is not free_leg))
			if self.are_legs_adjacent(free_leg, target_leg):
				leg_pairs.append({"free": free_leg, "target": target_leg})
		return leg_pairs

	def is_tri_good(self, p1, p2, p3, margin):
		side_length_1 = np.linalg.norm(p3 - p1)
		side_length_2 = np.linalg.norm(p3 - p2)
		return (abs(side_length_1 - side_length_2) < margin)

	def move_a_leg(self, direction_v):
		for leg_pair in self.get_leg_pairs(direction_v):
			print(leg_pair)
			stable_side = list((leg for leg in [0, 1, 2, 3] if leg is not leg_pair["target"] and leg is not leg_pair["free"]))
			if not self.is_tri_good(self.legs[stable_side[0]]["pos"], self.legs[stable_side[1]]["pos"], self.legs[leg_pair["free"]]["pos"], 1) and np.linalg.norm(self.legs[leg_pair["target"]]["pos"] - self.legs[leg_pair["free"]]["pos"]) > 1:
				leg_direction_u = unit_vector(self.legs[leg_pair["target"]]["pos"] - self.legs[leg_pair["free"]]["pos"])
				if angle_between(leg_direction_u, direction_v) < math.pi/2:
					self.legs[leg_pair["free"]]["pos"] += leg_direction_u * 3.5
				else:
					self.legs[leg_pair["free"]]["pos"] += direction_v * 3.5
			#elif np.linalg.norm(self.legs[leg_pair["target"]]["pos"] - self.legs[leg_pair["free"]]["pos"]) > 0 and self.is_tri_good(self.legs[stable_side[0]]["pos"], self.legs[stable_side[1]]["pos"], self.legs[leg_pair["target"]]["pos"], 1):
			#	self.legs[leg_pair["target"]]["pos"] += unit_vector(direction_v) * 3
			elif np.linalg.norm(self.legs[leg_pair["target"]]["pos"] - self.center["pos"]) < 60:
				self.legs[leg_pair["target"]]["pos"] += unit_vector(direction_v) * 3.5
				#allow for double replacement?
			else:
				print("no leg movement here?")
			break #temp

			#need to control real center vs ideal center
				#both in terms of not going too fast and in terms of not staying perfectly straight in order to balance
			#work on stopping movement when condidtion hits and actually start moving other leg
			



#locate free leg (there might be two)
#for each free leg:
	#check if free leg is replacing or moving
		#if moving - move to create ideal triangle
	#else locate target leg (leg that vector of movement points towards from center of triangle)??
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

#x+y%3 == 2 or 1
#0 12 12 12
#1 03 14 11
#2 03 25 22
#3 12 45 12

#midstep position and full step positions
#switch axis (90 degrees) after midstep, use original leg order. switch after full step, use new leg order. switch direction, reverse leg order
#rotate (45 degrees or less) - pick a leg to rotate from. move other three, starting from the back leg. back to middle, middle to front, front forward in new direction
#combine switch axis and rotate for 45 to 135 either direction. combine switch direction for 135 to 180 either direction

#at some point try to twist body based on leg position in order to face the right direction

#algo is based on leg replacement principle. replace one leg with the next in order to free the front leg. order of replacement depends on direction
#amount of rotation drives which of the two adjacent legs the free leg moves closest to
#straight is replace, move, replace, move. rotate is replace, replace, move. in order to shift the center, the algo must try to predict which leg will be free next