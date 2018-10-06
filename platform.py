import pygame


class Platform:
    width = 32 * 4
    height = 32

    image = pygame.image.load('resources/img/platform-32.png')
    shakeCoords = [10, -10, -5, 8, -3, 5, -2, 5, 1, -1, 0]

    def __init__(self, display, x, y):
        self.x = x
        self.y = y
        self.display = display
        self.shakeIndex = -1

    def draw(self):
        y = self.y
        if not self.shakeIndex == -1:
            y = y + self.shakeCoords[self.shakeIndex]
            self.shakeIndex = self.shakeIndex + 1
            if self.shakeIndex >= len(self.shakeCoords):
                self.shakeIndex = -1

        self.display.blit(Platform.image, (self.x, y))

    def shake(self):
        self.shakeIndex = 0
