import math

def cart2pol(x, y):
    r = math.sqrt(x**2 + y**2)
    t = math.atan2(y, x)
    return(r, t)

def pol2cart(r, t):
    x = r * math.cos(t)
    y = r * math.sin(t)
    return(x, y)

class IK():
	R1 = 47
	R2 = 50.5
	R3 = 95
	S = 108

	def __init__(self):
		pass

	def calc(self, leg, x, y, z):
		x = x - leg[2]
		y = y - leg[3]
		r, t = cart2pol(x, y)
		#print(r)
		#if(math.sqrt(x**2 + y**2 + z**2) > self.R1 + self.R2 + self.R3 or math.degrees(t) * leg[0] + leg[1] < 0 or math.degrees(t) * leg[0] + leg[1] > 180):
			#return None, None, None
			#return "Target out of range"
		t1 = math.degrees(t) * leg[0] + leg[1]
		temp = math.sqrt(x**2 + y**2) - self.R1
		r, T = cart2pol(temp, z)
		print(r, T)
		if r > 145.5:
			r = 145.5
		if r < 45.5:
			r = 45.5
		t3 = 225 - math.degrees(math.acos((self.R2**2 + self.R3**2 - r**2)/(2 * self.R2 * self.R3))) #r must be between 44.5 and 145.5 (actually 70, because t2 won't go less than 45 degrees)
		Y = math.acos((self.R2**2 - self.R3**2 + r**2)/(2 * self.R2 * r))
		t2 = math.degrees(T + Y) + 90 #?
		print(math.degrees(t), math.degrees(T + Y), math.degrees(math.acos((self.R2**2 + self.R3**2 - r**2)/(2 * self.R2 * self.R3))))
		print(round(t1, 2)%360, round(t2, 2)%360, round(t3, 2)%360)
		return round(t1, 2)%360, round(t2, 2)%360, round(t3, 2)%360