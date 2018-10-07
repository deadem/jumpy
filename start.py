from input import Input
from platform import Platform, Vanish, Moving
from manager import Manager
import math
import pygame
import random

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

resolution = { 'width': 800, 'height': 900 }

display = pygame.display.set_mode((resolution['width'],resolution['height']))
pygame.display.set_caption('Bumpy')
clock = pygame.time.Clock()

bumpyImage = pygame.image.load('resources/img/bumpy-32.png')
backgroundImage = pygame.image.load('resources/img/background.jpg')
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
        self.lastY = min(-self.y / 2, -25)
        self.maxY = 25
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
lastVanish = False
for m in range(0, 100):
    x = 32 * 4 * 1.2 * i + random.random() * 32 * 2
    y = 568 - 32 * 4 * 1.5 * m

    if random.random() < 0.3 and lastVanish == False:
        platform = Moving(x, y, resolution['width'])
        lastVanish = False
    elif random.random() < 0.3:
        lastVanish = True
        platform = Vanish(x, y)
    else:
        platform = Platform(x, y)
        lastVanish = False

    manager.add_platform(platform)
    if i > 0 and random.random() > 0.5 ** i:
        i = i - 1
    elif i < 5:
        i = i + 1

# platform1 = Platform(display, 0, 568)
# platform2 = Platform(display, 32 * 4, 568 - 32 * 4)
# platform3 = Platform(display, 32 * 4 * 2, 568 - 32 * 4 * 2)

p = 0
topOffset = 0
while True:
    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            quit()

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

    if y >= resolution['height'] - 64:
        offset = -40
        if topOffset <= -offset:
            state.jump()
        else:
            topOffset = topOffset + offset
            manager.move_view(offset)
        # if x >= 0 and x <= 32 * 4:
        #     platform1.shake()

    # if (x > 32 * 4) and (x < 32 * 4 + 32 * 4) and (y > 568 - 32 * 5) and (y < 568 - 32 * 3) and (state.y > 0):
    #     # platform2.shake()
    #     state.jump()

    state.updateY()
    state.updateX()

    coordinates['x'] = state.x
    coordinates['y'] = min(resolution['height'], y + state.y)

    display.fill((0, 0, 0))
    display.blit(backgroundImage, (0, 0))

    top = 200
    offset = top - coordinates['y']
    if offset > 0:
        coordinates['y'] = top
        manager.move_view(offset)
        topOffset = topOffset + offset

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
