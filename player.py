import pygame


class Player:
    x = 0
    y = 0
    ticks = 0
    lastY = 0
    lastX = 0
    maxY = 20

    def move_x(self, value):
        self.x = self.x + value * 10

    def jump(self):
        self.lastY = min(-self.y / 2, -25)
        self.maxY = 25
        self.ticks = pygame.time.get_ticks() / 100

    def tick(self):
        ticks = pygame.time.get_ticks() / 100
        self.y = min(self.maxY, self.lastY + (9.8 * (self.ticks - ticks) ** 2) / 4)
