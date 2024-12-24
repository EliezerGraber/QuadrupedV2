import turtle
from UI import UI
from Robot import Robot
import asyncio
import keyboard
import numpy as np

async def main():
	ui = UI(800, 800)
	ui.sc.bgcolor("black")
	robot = Robot(np.array([0, 0]), 50) #np.array([0, 0]), 50, 75, 0 #196?
	ui.bind_movement(robot.move)

	while True:
		ui.t.clear()
		legs, center, ideal_center, control_center, tris = robot.update()
		for triangle in tris:
			ui.draw_triangle(legs[triangle[0]]["pos"], legs[triangle[1]]["pos"], legs[triangle[2]]["pos"], legs[triangle[2]]["color"])
		for leg in legs:
			ui.draw_point(leg["pos"], 5, leg["color"])
		ui.draw_point(center["pos"], 5, center["color"])
		ui.draw_point(ideal_center["pos"], 5, ideal_center["color"])
		ui.draw_point(control_center["pos"], 5, control_center["color"])
		ui.update()
		if keyboard.is_pressed("Esc"):
			break

if __name__ == "__main__":
	asyncio.run(main())