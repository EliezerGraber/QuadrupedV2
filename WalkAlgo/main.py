import turtle
from UI import UI
from Robot import Robot
import asyncio
import keyboard
from utils import *

async def main():
	ui = UI(1000, 1000)
	ui.sc.bgcolor("black")
	robot = Robot(vector2(0, 0), 170) #np.array([0, 0]), 50, 75, 0 #196?
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
		#print(robot.get_legs()[0].x, robot.get_legs()[0].y) #br
		#print(robot.get_legs()[1].x, robot.get_legs()[1].y) #fr
		#print(robot.get_legs()[2].x, robot.get_legs()[2].y) #bl
		#print(robot.get_legs()[3].x, robot.get_legs()[3].y) #fl
		#print("br", robot.get_legs()[0].x, robot.get_legs()[0].y) #br
		#print("fr", robot.get_legs()[1].x, robot.get_legs()[1].y) #fr
		#print("bl", robot.get_legs()[2].x, robot.get_legs()[2].y) #bl
		#print("fl", robot.get_legs()[3].x, robot.get_legs()[3].y) #fl
		if keyboard.is_pressed("Esc"):
			break

if __name__ == "__main__":
	asyncio.run(main())