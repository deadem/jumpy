import pygame

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

