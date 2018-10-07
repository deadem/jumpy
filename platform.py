import pygame
import random

class Type:
    regular = 1
    vanish = 2

class Platform:
    width = 32 * 4
    height = 16

    image = pygame.image.load('resources/img/platform-32.png')
    shakeCoords = [10, -10, -5, 8, -3, 5, -2, 5, 1, -1, 0]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shakeIndex = -1

    def draw(self, display):
        y = self.y
        if not self.shakeIndex == -1:
            y = y + self.shakeCoords[self.shakeIndex]
            self.shakeIndex = self.shakeIndex + 1
            if self.shakeIndex >= len(self.shakeCoords):
                self.shakeIndex = -1

        display.blit(self.image, (self.x, y))

    def hit(self):
        self.shakeIndex = 0

    def can_hit(self):
        return True

class Vanish(Platform):
    def __init__(self, x, y):
        self.image = pygame.image.load('resources/img/platform-white-32.png')
        self.alpha = 255
        self.fade = True
        super().__init__(x, y)

    def draw(self, display):
        super().draw(display)
        if not self.alpha == 255:
            self.alpha = min(255, self.alpha + (-10 if self.fade else 10))
            if self.alpha <= 0:
                self.fade = False

        self.image.set_alpha(self.alpha)

    def hit(self):
        super().hit()
        self.fade = True
        self.alpha = 254

    def can_hit(self):
        return self.alpha == 255

class Moving(Platform):

    def __init__(self, x, y, maxX):
        self.stepLimit = 64 + 100 * random.random()
        self.maxX = maxX
        self.steps = self.stepLimit / 2
        self.offset = 2 + random.random() * 8

        self.image = pygame.image.load('resources/img/platform-blue-32.png')
        super().__init__(x, y)

    def draw(self, display):
        self.x = self.x + self.offset
        self.steps = self.steps + 1
        if self.x < 0:
            self.offset = abs(self.offset)
            self.steps = 0
        elif self.x + self.width > self.maxX:
            self.offset = -abs(self.offset)
            self.steps = 0
        elif self.steps > self.stepLimit:
            self.offset = self.offset * -1
            self.steps = 0

        super().draw(display)
