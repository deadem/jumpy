import pygame

pygame.init()

resolution = { 'width': 800, 'height': 600 }

display = pygame.display.set_mode((resolution['width'],resolution['height']))
pygame.display.set_caption('Bumpy')
clock = pygame.time.Clock()

bumpyImage = pygame.image.load('resources/img/bumpy-32.png')

joystick = pygame.joystick.Joystick(0)
joystick.init()

class State:
	x = 0
	y = 0
	ticks = 0
	lastY = 0

	def updateX(self, value):
		if abs(value) < 0.3:
			self.x = 0
		elif value > 0.5:
			self.x = 1
		elif value < -0.5:
			self.x = -1

	def updateY(self):
		ticks = pygame.time.get_ticks() / 100
		self.y = self.lastY + (9.8 * (self.ticks - ticks) ** 2) / 4
		if self.y > 20:
			self.y = 20
		# self.ticks = ticks

	def jump(self):
		self.lastY = -20
		self.ticks = pygame.time.get_ticks() / 100

state = State()
coordinates = { 'x': 400, 'y': 0 }

quit = False
while not quit:
	for event in pygame.event.get():
		quit = quit | event.type == pygame.QUIT
		print(event)

		if event.type == pygame.JOYAXISMOTION:
			if event.axis == 0:
				state.updateX(event.value)
			# if event.axis == 1:
			# 	coordinates['y'] = coordinates['y'] + event.value * 10

	if coordinates['y'] > 550:
		state.jump()

	state.updateY()

	coordinates['x'] = coordinates['x'] + state.x * 10
	coordinates['y'] = coordinates['y'] + state.y

	display.fill((0, 0, 0))
	display.blit(bumpyImage, (coordinates['x'], coordinates['y']))

	pygame.display.update()
	clock.tick(60) # FPS

pygame.quit()
