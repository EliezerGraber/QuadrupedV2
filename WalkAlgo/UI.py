import tkinter as tk
import turtle

class UI():
	style = ('Arial', 14, 'normal')

	def __init__(self, x, y):
		self.root = tk.Tk()
		self.root.title("Quadrupedal Walking Simulator")
		self.canvas = turtle.ScrolledCanvas(self.root, x, y)
		self.root.resizable(False, False)
		self.canvas.pack()
		self.sc = turtle.TurtleScreen(self.canvas)
		self.t = turtle.RawTurtle(self.sc)
		self.t.speed(0)
		self.sc.tracer(False)
		self.t.ht()
		self.t.penup()

	def draw_point(self, p, r, color):
		self.t.goto(p[0], p[1])
		self.t.dot(2*r, color)

	def draw_triangle(self, p0, p1, p2, color):
		self.t.goto(p0[0], p0[1])
		self.t.pendown()
		self.t.begin_fill()
		self.t.color(color)
		self.t.goto(p1[0], p1[1])
		self.t.goto(p2[0], p2[1])
		self.t.goto(p0[0], p0[1])
		self.t.end_fill()
		self.t.penup()

	def update(self):
		self.sc.update()

	def bind_movement(self, movement):
		self.root.bind('<Up>', lambda event: movement(event.keysym))
		self.root.bind('<Down>', lambda event: movement(event.keysym))
		self.root.bind('<Right>', lambda event: movement(event.keysym))
		self.root.bind('<Left>', lambda event: movement(event.keysym))