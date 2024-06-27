import turtle
from UI import UI
from Robot import Robot
import asyncio
import keyboard
import numpy as np

async def main():
	ui = UI(600, 600)
	ui.sc.bgcolor("black")
	robot = Robot(ui, np.array([0, 0]), 50, 75)

	while True:
		ui.t.clear()
		robot.draw()
		ui.update()
		if keyboard.is_pressed("Esc"):
			break

if __name__ == "__main__":
	asyncio.run(main())