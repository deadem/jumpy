import pygame
import math

pygame.init()

resolution = { 'width': 800, 'height': 600 }

display = pygame.display.set_mode((resolution['width'],resolution['height']))
pygame.display.set_caption('Bumpy')
clock = pygame.time.Clock()

bumpyImage = pygame.image.load('resources/img/bumpy-32.png')
platformImage = pygame.image.load('resources/img/platform-32.png')

joystick = pygame.joystick.Joystick(0)
joystick.init()

class State:
    x = 0
    y = 0
    ticks = 0
    lastY = 0
    lastX = 0
    targetX = 0
    maxY = 20

    def center(self):
        return int(self.x / (32 * 4)) * (32 * 4) + (32 * 2) - 32 / 2

    def updateX(self):
        if not self.targetX == self.x:
            self.x = self.x + math.copysign(1, self.targetX - self.x) * 8

    def moveX(self, value):
        if self.y > 0 or abs(value) < 0.3 or not (self.targetX == self.x):
            # self.x = 0
            pass
        elif value > 0.5:
            self.targetX = self.center() + 32 * 4
        elif value < -0.5:
            self.targetX = self.center() - 32 * 4

    def updateY(self):
        ticks = pygame.time.get_ticks() / 100
        self.y = min(self.maxY, self.lastY + (9.8 * (self.ticks - ticks) ** 2) / 4)

    def jump(self):
        self.lastY = min(-self.y / 2, -20)
        self.maxY = 20
        self.ticks = pygame.time.get_ticks() / 100

    def power(self):
        if self.y < 0:
            return
        self.lastY = min(20, self.lastY)
        self.maxY = 80


state = State()
coordinates = { 'x': 0, 'y': 0 }

p = 0

quit = False
while not quit:
    for event in pygame.event.get():
        quit = quit | event.type == pygame.QUIT
        print(event)

        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                state.moveX(event.value)
            # if event.axis == 1:
            #     coordinates['y'] = coordinates['y'] + event.value * 10

        if event.type == pygame.JOYBUTTONDOWN:
            state.power()

    x = coordinates['x']
    y = coordinates['y']

    if y > 534:
        state.jump()

    if (x > 32 * 4) and (x < 32 * 4 + 32 * 4) and (y > 568 - 32 * 5) and (y < 568 - 32 * 3) and (state.y > 0):
        state.jump()

    state.updateY()
    state.updateX()

    coordinates['x'] = state.x
    coordinates['y'] = min(535, y + state.y)

    display.fill((0, 0, 0))
    display.blit(bumpyImage, (coordinates['x'], coordinates['y']))

    display.blit(platformImage, (0, 568))

    display.blit(platformImage, (32 * 4, 568 - 32 * 4))

    pygame.display.update()
    clock.tick(60) # FPS

pygame.quit()
