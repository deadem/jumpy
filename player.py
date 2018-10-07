import pygame
from screen import Screen

class Player:
    width = 32
    height = 32
    x = 0
    y = 0
    ticks = 0
    lastY = 0
    jumpY = 25
    canJump = True
    fallDown = 0


    def move_x(self, value):
        self.x = self.x + value * 10
        self.x = max(0, min(Screen.width - Player.width, self.x))

    def jump(self):
        self.lastY = min(-self.y / 2, -25)
        self.ticks = pygame.time.get_ticks() / 100

    def tick(self):
        ticks = pygame.time.get_ticks() / 100
        self.y = min(self.jumpY, self.lastY + (9.8 * (self.ticks - ticks) ** 2) / 4)

    def can_jump(self):
        if not self.canJump and self.fallDown <= pygame.time.get_ticks():
            self.canJump = True
        return self.canJump

    def fall(self):
        self.fallDown = pygame.time.get_ticks() + 1000
        self.canJump = False

