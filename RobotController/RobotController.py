from Servo import Servo
from IK import IK
import asyncio

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

		self.fr1 = Servo(18, 20, 123)
		self.fr2 = Servo(19, 26, 127)
		self.fr3 = Servo(21, 26, 127)

		self.fl1 = Servo(25, 23, 123)
		self.fl2 = Servo(33, 23, 123)
		self.fl3 = Servo(32, 20, 123)

		self.bl1 = Servo(13, 21, 132)
		self.bl2 = Servo(27, 26, 126)
		self.bl3 = Servo(26, 25, 123)

		self.br1 = Servo(4, 20, 123)
		self.br2 = Servo(16, 25, 123)
		self.br3 = Servo(17, 26, 131)

		self.legs = [[FR, [self.fr1, self.fr2, self.fr3]],
				[FL, [self.fl1, self.fl2, self.fl3]],
				[BL, [self.bl1, self.bl2, self.bl3]],
				[BR, [self.br1, self.br2, self.br3]]] #pointer or copy?

	async def cue_move_leg_tasks(self, leg, x, y, z, delta = 0):
		t1, t2, t3 = self.ik.calc(self.legs[leg][0], x, y, z)
		if t1 is not None:
			tasks = [0, 0, 0]
			tasks[0] = asyncio.create_task(self.legs[leg][1][0].move(t1, delta))
			tasks[1] = asyncio.create_task(self.legs[leg][1][1].move(t2, delta))
			tasks[2] = asyncio.create_task(self.legs[leg][1][2].move(t3, delta))
			return tasks
		return None

	async def move_leg(self, leg, x, y, z, delta = 0):
		tasks = await self.cue_move_leg_tasks(self, leg, x, y, z, delta)
		for task in tasks:
			await task

	async def stand(self):
		tasks = await self.cue_move_leg_tasks(0, 80, 180, -60, 1)
		tasks.append(await self.cue_move_leg_tasks(1, -80, 180, -60, 1))
		tasks.append(await self.cue_move_leg_tasks(2, -80, -180, -60, 1))
		tasks.append(await self.cue_move_leg_tasks(3, 80, -180, -60, 1))
		for task in tasks:
			await task

	async def reset(self):
		tasks = await self.cue_move_leg_tasks(0, 80, 180, -25)
		tasks.append(await self.cue_move_leg_tasks(1, -80, 180, -25))
		tasks.append(await self.cue_move_leg_tasks(2, -80, -180, -25))
		tasks.append(await self.cue_move_leg_tasks(3, 80, -180, -25))
		for task in tasks:
			await task
			