from Servo import Servo
from IK import IK
import asyncio
from Robot import Robot
from utils import *

FR = [1, 60, 54, 54]
FL = [1, -60, -54, 54]
BL = [1, -120, -54, -54]
BR = [1, 120, 54, -54]

async def aio_all(seq):
	for f in asyncio.as_completed(seq):
		await f

class RobotController():
	def __init__(self):
		self.ik = IK()
		self.robot = Robot(vector2(0, 0), 155)

		self.fr1 = Servo(18, 20, 128)
		self.fr2 = Servo(19, 26, 127)
		self.fr3 = Servo(21, 26, 127)

		self.fl1 = Servo(25, 20, 125)
		self.fl2 = Servo(33, 23, 123)
		self.fl3 = Servo(32, 20, 123)

		self.bl1 = Servo(13, 21, 132)
		self.bl2 = Servo(27, 26, 126)
		self.bl3 = Servo(26, 25, 123)

		self.br1 = Servo(4, 22, 132)
		self.br2 = Servo(16, 25, 123)
		self.br3 = Servo(17, 26, 131)

		self.legs = [[FR, [self.fr1, self.fr2, self.fr3]],
				[FL, [self.fl1, self.fl2, self.fl3]],
				[BL, [self.bl1, self.bl2, self.bl3]],
				[BR, [self.br1, self.br2, self.br3]]] #pointer or copy?

		asyncio.run(self.float_pos())

	async def move_seg(self, x, y):
		self.robot.move(x, y)
		free = self.robot.free_leg

		tasks = [
			self.cue_move_leg_tasks(0, self.robot.get_legs()[1].x, self.robot.get_legs()[1].y, -30 if free == 1 else -60),
			self.cue_move_leg_tasks(1, self.robot.get_legs()[3].x, self.robot.get_legs()[3].y, -30 if free == 3 else -60),
			self.cue_move_leg_tasks(2, self.robot.get_legs()[2].x, self.robot.get_legs()[2].y, -30 if free == 2 else -60),
			self.cue_move_leg_tasks(3, self.robot.get_legs()[0].x, self.robot.get_legs()[0].y, -30 if free == 0 else -60)
		]
		for task in tasks:
			await task
		await asyncio.sleep_ms(1)


	async def move_forward(self, x):
		for i in range(x):
			#print(i + 1, "/", x)
			await self.move_seg(0, 1)
			#self.robot.move(0, 1)
			#free = self.robot.free_leg
			#print(free)
			#print("br", self.robot.get_legs()[0].x, self.robot.get_legs()[0].y) #br 3
			#print("fr", self.robot.get_legs()[1].x, self.robot.get_legs()[1].y) #fr 0
			#print("bl", self.robot.get_legs()[2].x, self.robot.get_legs()[2].y) #bl 2
			#print("fl", self.robot.get_legs()[3].x, self.robot.get_legs()[3].y) #fl 1
			#tasks = await self.cue_move_leg_tasks(0, self.robot.get_legs()[1].x, self.robot.get_legs()[1].y, -35 if free == 1 else -60)
			#tasks.append(await self.cue_move_leg_tasks(1, self.robot.get_legs()[3].x, self.robot.get_legs()[3].y, -35 if free == 3 else -60))
			#tasks.append(await self.cue_move_leg_tasks(2, self.robot.get_legs()[2].x, self.robot.get_legs()[2].y, -35 if free == 2 else -60))
			#tasks.append(await self.cue_move_leg_tasks(3, self.robot.get_legs()[0].x, self.robot.get_legs()[0].y, -35 if free == 0 else -60))
			#for task in tasks:
			#	await task
			#await asyncio.sleep_ms(10)
			if i%50 == 0:
				print(i, "/", x)

	async def cue_move_leg_tasks(self, leg, x, y, z, delta = 0):
		#print(leg)
		t1, t2, t3 = self.ik.calc(self.legs[leg][0], x, y, z)
		if t1 is not None:
			tasks = [0, 0, 0]
			tasks[0] = asyncio.create_task(self.legs[leg][1][0].move(t1, delta))
			tasks[1] = asyncio.create_task(self.legs[leg][1][1].move(t2, delta))
			tasks[2] = asyncio.create_task(self.legs[leg][1][2].move(t3, delta))
			return tasks
		return None

	async def move_leg(self, leg, x, y, z, delta = 0):
		tasks = await self.cue_move_leg_tasks(leg, x, y, z, delta)
		for task in tasks:
			await task

	async def stand(self): #170 ideal distance
		tasks = await self.cue_move_leg_tasks(0, 110, 110, -65, 0.4)
		tasks.append(await self.cue_move_leg_tasks(1, -110, 110, -65, 0.4))
		tasks.append(await self.cue_move_leg_tasks(2, -110, -110, -65, 0.4))
		tasks.append(await self.cue_move_leg_tasks(3, 110, -110, -65, 0.4))
		for task in tasks:
			await task

	async def reset(self):
		tasks = await self.cue_move_leg_tasks(0, 140, 140, -25, 0.4)
		tasks.append(await self.cue_move_leg_tasks(1, -140, 140, -25, 0.4))
		tasks.append(await self.cue_move_leg_tasks(2, -140, -140, -25, 0.4))
		tasks.append(await self.cue_move_leg_tasks(3, 140, -140, -25, 0.4))
		for task in tasks:
			await task
			
	async def float_pos(self): #212
		tasks = await self.cue_move_leg_tasks(0, 150, 150, -5, 0.4)
		tasks.append(await self.cue_move_leg_tasks(1, -150, 150, -5, 0.4))
		tasks.append(await self.cue_move_leg_tasks(2, -150, -150, -5, 0.4))
		tasks.append(await self.cue_move_leg_tasks(3, 150, -150, -5, 0.4))
		for task in tasks:
			await task