import pygame


class Platform:
    x = 0
    y = 0
    image = pygame.image.load('resources/img/platform-32.png')
    shake = [10, -10, -5, 8, -3, 5, -2, 5, 1, -1, 0]

    def __init__(self, display, x, y):
        self.x = x
        self.y = y
        self.display = display

    def draw(self):
        self.display.blit(Platform.image, (self.x, self.y))
