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
		self.free_leg = 0
		self.balance_safety = balance_safety
		self.ready_to_switch = True

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
			return None

	def find_target_leg(self, direction_v, triangle):
		print(triangle)
		side = find_side_of_triangle(self.legs, triangle, direction_v, self.center["pos"])
		print(side, direction_v, self.legs[side[0]]["pos"] - self.legs[side[1]]["pos"])
		if np.dot(self.legs[side[0]]["pos"] - self.legs[side[1]]["pos"], direction_v) > 0:
			return side[1], side
		else:
			return side[0], side

	def move(self, direction):
		direction_v = np.array([int(direction == "Right") - int(direction == "Left"), int(direction == "Up") - int(direction == "Down")])
		norm = np.linalg.norm(direction_v)
		direction_u = direction_v/norm
		
		if self.ready_to_switch:
			self.adjusted_direction_v, self.pair = self.leg_switch(direction_v)
			self.ready_to_switch = False
		else:
			self.ready_to_switch = self.leg_move(self.adjusted_direction_v, self.pair)

		self.ideal_center["pos"] = self.ideal_center["pos"] + direction_v/2 #+=?
		self.center["pos"] = self.center["pos"] + direction_v/2 #only update real center if moving wont disrupt the active triangle

	def are_legs_adjacent(self, l1, l2):
		return (l1 + l2) %3 == 1 or (l1 + l2) %3 == 2

	def get_leg_pairs(self, direction_v):
		tris = self.balance_check()
		free_legs = self.find_free_legs(tris)
		if free_legs == None:
			free_legs = [farthest_vector(direction_v, [leg["pos"] for leg in self.legs])] #should an approach like this be used all the time?
			tris = [[self.legs[leg]["pos"] for leg in [0, 1, 2, 3] if leg != free_legs[0]]]
		leg_pairs = [];
		for i, free_leg in enumerate(free_legs):
			target_leg, side = self.find_target_leg(direction_v, [leg for leg in [0, 1, 2, 3] if leg != free_leg])
			print(self.are_legs_adjacent(free_leg, target_leg))
			x = np.dot(self.legs[target_leg]["pos"] - self.legs[free_leg]["pos"], direction_v)
			print(x)
			if 0 < x < 3 or x < -75: #70? 90? issues because center isn't fast enough. if it is sped up uniformly this causes other issues. work on variable speed
				continue
			if self.are_legs_adjacent(free_leg, target_leg) and np.dot(direction_v, self.legs[target_leg]["pos"] - self.legs[free_leg]["pos"]) > 0:
				cores = [leg for leg in [0, 1, 2, 3] if leg != free_leg and leg != target_leg]
				leg_pairs.append({"free": free_leg, "target": target_leg, "cores": cores, "tri": tris[i]})
			else:
				cores = [leg for leg in [0, 1, 2, 3] if leg != free_leg]
				leg_pairs.append({"free": free_leg, "target": None, "cores": side, "tri": tris[i]})
		return leg_pairs

	def is_tri_good(self, p1, p2, p3, margin):
		side_length_1 = np.linalg.norm(p3 - p1)
		side_length_2 = np.linalg.norm(p3 - p2)
		return (abs(side_length_1 - side_length_2) < margin)

	def leg_switch(self, direction_v):
		leg_pairs = self.get_leg_pairs(direction_v)
		tris = []
		print(leg_pairs)
		for pair in leg_pairs:
			tris.append(pair["tri"])
		index = closest_to_equilateral(tris)
		leg_pair = leg_pairs[index]
		print(leg_pair)
		#for leg_pair in self.get_leg_pairs(direction_v):
		if leg_pair["target"] != None:
			if not self.is_tri_good(self.legs[leg_pair["cores"][0]]["pos"], self.legs[leg_pair["cores"][1]]["pos"], self.legs[leg_pair["free"]]["pos"], 2):# and np.linalg.norm(self.legs[leg_pair["target"]]["pos"] - self.legs[leg_pair["free"]]["pos"]) > 1:
				leg_direction_u = unit_vector(self.legs[leg_pair["target"]]["pos"] - self.legs[leg_pair["free"]]["pos"])
				if abs(angle_between(leg_direction_u, direction_v)) < math.pi/2: #this may need to be absolute value of angle
					adjusted_direction_v = leg_direction_u * 2.4
				else:
					adjusted_direction_v = unit_vector(direction_v) * 2.4 #speed needs to be a universal variable, but depended on distance (sine)
				self.free_leg = leg_pair["free"]
				#break
			elif np.linalg.norm(self.legs[leg_pair["target"]]["pos"] - self.center["pos"]) < 60:
				adjusted_direction_v = unit_vector(direction_v) * 2.4
				self.free_leg = leg_pair["target"]
				#allow for double replacement?
				#break
			else:
				print("no leg movement here?")
			#break #temp
		else:
			adjusted_direction_v = unit_vector(direction_v) * 2.4 #maybe?
			self.free_leg = leg_pair["free"]
		
		return adjusted_direction_v, leg_pair

	def leg_move(self, direction_v, pair):
		self.legs[self.free_leg]["pos"] += direction_v
		a = np.linalg.norm(self.legs[self.free_leg]["pos"] - self.legs[pair["cores"][0]]["pos"])
		b = np.linalg.norm(self.legs[self.free_leg]["pos"] - self.legs[pair["cores"][1]]["pos"])
		
		#c = np.linalg.norm(self.legs[pair["free"]]["pos"] - self.legs[pair["target"]]["pos"])
		#d = 70#np.linalg.norm(self.legs[pair["cores"][0]]["pos"] - self.legs[pair["cores"][1]]["pos"])
		
		#v = max_p - self.legs[self.free_leg]["pos"]
		#if abs(angle_between(v, direction_v)) < math.pi/2:
		if pair["target"] == None:
			print(round(a, 2), round(b, 2))
			if abs(a - b) > 3:
				return False
		elif self.free_leg == pair["free"]:
			print(round(a, 2), round(b, 2), round(np.linalg.norm(self.legs[pair["target"]]["pos"] - self.legs[self.free_leg]["pos"]), 2))
			if abs(a - b) > 3 and np.linalg.norm(self.legs[pair["target"]]["pos"] - self.legs[self.free_leg]["pos"]) > 3:
				return False
		elif self.free_leg == pair["target"]:
			#print(round(c, 2), round(d, 2))
			#if abs(c - d) > 3:
			print("target leg is free")
			return False
		#if (abs(a - b) > 5 and self.free_leg == pair["free"]) or (abs(c - d) > 5 and self.free_leg == pair["target"]): #if moving free, if target, its closer core and free, or core to core and free to target
		#	return False
		return True

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