import pygame
import numpy as np
import math

screen = pygame.display.set_mode((800, 600))

running = True

circles = []

class Circle:
	def __init__(self, x, y, radius, filled=False, outline=None):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = (255, 0, 0)
		self.points = []
		self.filled = filled
		self.generate_points()
		self.points = list(set(self.points))

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
		self.points = []
		for degree in np.arange(0, 360, 1):
			self.points.append((self.x + math.cos(degree) * self.radius, self.y + math.sin(degree) * self.radius))

test_circle = Circle(250, 250, 100, filled=False,outline=[2,(255,0,0)])

clock = pygame.time.Clock()

while running:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	test_circle.draw()
	pygame.display.flip()
	clock.tick(30)