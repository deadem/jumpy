from input import Input
from platform import Platform
from manager import Manager
import math
import pygame
import random

pygame.init()

resolution = { 'width': 800, 'height': 600 }

display = pygame.display.set_mode((resolution['width'],resolution['height']))
pygame.display.set_caption('Bumpy')
clock = pygame.time.Clock()

bumpyImage = pygame.image.load('resources/img/bumpy-32.png')
userInput = Input()


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
        if self.targetX and not self.targetX == self.x:
            self.x = self.x + math.copysign(1, self.targetX - self.x) * 8

    def moveX(self, value):
        self.x = self.x + value * 10

    def updateY(self):
        ticks = pygame.time.get_ticks() / 100
        self.y = min(self.maxY, self.lastY + (9.8 * (self.ticks - ticks) ** 2) / 4)

    def jump(self):
        self.lastY = min(-self.y / 2, -20)
        self.maxY = 20
        self.ticks = pygame.time.get_ticks() / 100
        self.targetX = 0

    def power(self):
        if self.y < 0:
            return
        self.lastY = min(20, self.lastY)
        self.maxY = 80


state = State()
coordinates = { 'x': 0, 'y': 0 }

manager = Manager(display)

i = 0
for m in range(0, 100):
    manager.add_platform(32 * 4 * i, 568 - 32 * 4 * 1.5 * m)
    if i > 0 and random.random() > 0.5 ** i:
        i = i - 1
    elif i < 5:
        i = i + 1

# platform1 = Platform(display, 0, 568)
# platform2 = Platform(display, 32 * 4, 568 - 32 * 4)
# platform3 = Platform(display, 32 * 4 * 2, 568 - 32 * 4 * 2)

p = 0

quit = False
while not quit:
    for event in pygame.event.get():
        quit = quit | event.type == pygame.QUIT
        print(event)

        userInput.event(event)


        # if event.type == pygame.JOYAXISMOTION:
        #     if event.axis == 0:
        #         state.moveX(event.value)
        #     # if event.axis == 1:
        #     #     coordinates['y'] = coordinates['y'] + event.value * 10

        # if event.type == pygame.JOYBUTTONDOWN:
        #     state.power()

    state.moveX(userInput.test(x=True))

    x = coordinates['x']
    y = coordinates['y']

    if y >= 600:
        # if x >= 0 and x <= 32 * 4:
        #     platform1.shake()
        state.jump()

    # if (x > 32 * 4) and (x < 32 * 4 + 32 * 4) and (y > 568 - 32 * 5) and (y < 568 - 32 * 3) and (state.y > 0):
    #     # platform2.shake()
    #     state.jump()

    state.updateY()
    state.updateX()

    coordinates['x'] = state.x
    coordinates['y'] = min(600, y + state.y)

    display.fill((0, 0, 0))

    top = 100
    offset = top - coordinates['y']
    if offset > 0:
        coordinates['y'] = top
        manager.move_view(offset)

    if manager.hit_test(coordinates['x'], coordinates['y'], state.y > 0):
        state.jump()
    manager.draw()

    display.blit(bumpyImage, (coordinates['x'], coordinates['y']))

    # platform1.draw()
    # platform2.draw()
    # platform3.draw()

    pygame.display.update()
    clock.tick(60) # FPS

pygame.quit()
