from Servo import Servo
from IK import IK

FR = [1, 60, 54, 54]
FL = [-1, 240, -54, 54]
BL = [-1, 420, -54, -54]
BR = [1, -120, 54, -54]

class RobotController():
	def __init__(self):
		ik = IK()

		fr1 = Servo(18, 20, 123)
		fr2 = Servo(19, 26, 127)
		fr3 = Servo(21, 26, 127)

		fl1 = Servo(25, 23, 123)
		fl2 = Servo(33, 23, 123)
		fl3 = Servo(32, 20, 123)

		bl1 = Servo(13, 21, 132)
		bl2 = Servo(27, 26, 126)
		bl3 = Servo(26, 26, 123)

		br1 = Servo(4, 20, 123)
		br2 = Servo(16, 25, 123)
		br3 = Servo(27, 26, 131)

		legs = [[FR, [fr1, fr2, fr3]],
				[FL, [fl1, fl2, fl3]],
				[BL, [bl1, bl2, bl3]],
				[BR, [br1, br2, br3]]]

	def move_leg(self, leg, x, y, z):
		t1, t2, t3 = ik(legs[leg][0], x, y, z)
		if t1 is not None:
		legs[leg][1][0].move(t1)
		legs[leg][1][1].move(t2)
		legs[leg][1][3].move(t3)
