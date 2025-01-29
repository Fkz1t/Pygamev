import pygame
import numpy as np
import math

screen = pygame.display.set_mode((800, 600))

running = True

circles = []

twoPi:float = math.pi*2.0

class Circle:
	def __init__(self, x, y, radius, filled=False, outline=None):
		self.x = x
		self.y = y
		self.radius = radius
		self.color:tuple[int,int,int] = (255, 0, 0)
		self.points:list = []
		self.filled:bool = filled
		self.generate_points()
		self.points:list = list(set(self.points))

		self.outline = outline

	def draw(self):
		if self.outline:
			for point in self.points:
				if not point[0] > screen.get_width() and not point[0] < 0 and not point[1] < 0 and not point[1] > screen.get_height():
					for x in range(self.outline[0] * 2):
						for y in range(self.outline[0] * 2):
							screen.set_at(
								(
									point[0] + -self.outline[0] + x, point[1] + -self.outline[0] + y
								),
									self.color
							)

					if self.filled:
						pygame.draw.line(screen, self.color, (self.x,self.y), point)

		else:
			for point in self.points:
				if not point[0] > screen.get_width() and not point[0] < 0 and not point[1] < 0 and not point[1] > screen.get_height():
					screen.set_at(point, self.color)

					if self.filled:
						pygame.draw.line(screen, self.color, (self.x, self.y), point)

	def generate_points(self):
		self.points:list = []
		for degree in np.arange(0, 360, 1):
			self.points.append((self.x + math.cos(degree) * self.radius, self.y + math.sin(degree) * self.radius))

"""
Class object of an Ellipse. It is really cool.
"""
class Ellipse:
	def __init__(self, pos, r1, r2, filled=False, outline=None):
		self.pos = pos
		self.r1 = r1
		self.r2 = r2
		self.filled = filled
		self.outline = outline
		self.deltaTheta = 0.0001
		self.numIntegrals = round(twoPi / self.deltaTheta)
		self.circ = 0.0
		self.dpt = 0.0
		self.points = []

	def find_circumference(self) -> float or int or None:
		theta = 0
		self.circ = 0.0
		for i in range(0, self.numIntegrals):
			theta += i * self.deltaTheta
			dpt = compute_dpt(self.r1, self.r2, theta)
			self.circ += dpt

		return self.circ

	def find_points(self, n=50) -> list or None:
		self.points = []

		self.find_circumference()

		nextpoint:int = 0
		run:float = 0.0
		theta:float = 0.0

		for i in range(0, self.numIntegrals):
			theta += self.deltaTheta
			subIntegral:float = n * run/self.circ

			if subIntegral > nextpoint:
				x:float = self.r1 * math.cos(theta)
				y:float = self.r2 * math.sin(theta)
				nextpoint += 1

				self.points.append((x,y))

			run += compute_dpt(self.r1, self.r2, theta)

		if self.points: return self.points
		else: return None

	def draw(self):
		for point in self.points:
			pygame.draw.circle(screen, (0,255,0), (point[0] + self.pos[0], point[1] + self.pos[1]), 1)


class Polygon:
	def __init__(self, points:list[tuple[int or float],tuple[int or float],tuple[int or float], tuple[int or float]], filled:bool=False, outline=None):
		self.points = points
		self.filled = filled
		self.outline = outline

class Rectangle:
	def __init__(self, x, y, width, height, filled=False, outline_width=1):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.filled = filled
		self.outline_width = outline_width
		self.top = bresenham(self.x, self.y, self.x + self.width, self.y)
		self.right = bresenham(self.x + self.width, self.y, self.x + self.width, self.y + self.height)
		self.left = bresenham(self.x, self.y + self.height, self.x, self.y)
		self.bottom = bresenham(self.x + self.width, self.y + self.height, self.x, self.y + self.height)
		self.fill = []
		for x in range(self.width):
			self.fill.append(bresenham(self.x + x, self.y, self.x + x, self.y + self.height))

	def draw(self, surface, color:tuple[int or float, int or float, int or float]):
		#top left to top right
		#pygame.draw.line(surface, color, (self.x, self.y), (self.x + self.width, self.y), self.outline_width)
		#top right to bottom right
		#pygame.draw.line(surface, color, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), self.outline_width)
		#bottom right to bottom left
		#pygame.draw.line(surface, color, (self.x + self.width, self.y + self.height), (self.x, self.y + self.height),
		#				 self.outline_width)
		#bottom left to top left
		#pygame.draw.line(surface, color, (self.x, self.y + self.height), (self.x, self.y),
		#				 self.outline_width)

		for point in self.top :
			surface.set_at(point, color)

		for point in self.right:
			surface.set_at(point, color)

		for point in self.left:
			surface.set_at(point, color)

		for point in self.bottom:
			surface.set_at(point, color)

		if self.filled:
			for row in self.fill:
				for point in row:
					surface.set_at(point, color)



def bresenham(x1, y1, x2, y2):
	"""
	Implements Bresenham's Line Algorithm.
	Returns a list of all points on the line as (x, y) tuples.
	"""
	points = []

	dx = abs(x2 - x1)
	dy = abs(y2 - y1)
	sx = 1 if x1 < x2 else -1
	sy = 1 if y1 < y2 else -1
	err = dx - dy

	while True:
		points.append((x1, y1))

		if x1 == x2 and y1 == y2:
			break

		e2 = 2 * err
		if e2 > -dy:
			err -= dy
			x1 += sx
		if e2 < dx:
			err += dx
			y1 += sy

	return points

"""
calculates the distance from the center of the ellipse to the point on the ellipse at the given theta plus π/2
"""
def compute_dpt(r1:float or int, r2:float or int, theta:float or int) -> float:
	dpt_sin:float = math.pow(r1 * math.sin(theta), 2.0)
	dpt_cos:float = math.pow(r2 * math.cos(theta), 2.0)

	dp:float = math.sqrt(dpt_sin + dpt_cos)

	return dp

test_circle:Circle = Circle(250, 250, 100, filled=False,outline=[2,(255,0,0)])

clock:pygame.time.Clock = pygame.time.Clock()

ellipse:Ellipse = Ellipse((250, 250), 1000, 200, filled=False)

ellipse.find_points(n=50)

rectangle:Rectangle = Rectangle(250, 100, 200, 200, filled=True, outline_width=1)

while running:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	ellipse.draw()

	test_circle.draw()
	rectangle.draw(screen, (255,255,255))
	pygame.display.flip()
	clock.tick(30)