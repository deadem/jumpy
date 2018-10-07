import pygame
import random


class Monster:
    width = 64
    height = 64
    alive = True
    sound = False
    bite = False
    image = pygame.image.load('resources/img/monster.png')

    def __init__(self, x, y, maxX):
        if not Monster.sound:
            Monster.sound = pygame.mixer.Sound('resources/sound/monster-hit.wav')
        if not Monster.bite:
            Monster.bite = pygame.mixer.Sound('resources/sound/bite.wav')
        self.x = x
        self.y = y
        self.maxX = maxX
        self.offset = 2 + random.random() * 8
        self.fall = -1

    def draw(self, display):
        if self.x + self.width >= self.maxX:
            self.offset = -abs(self.offset)
        if self.x <= 0:
            self.offset = abs(self.offset)

        self.x = self.x + self.offset
        if not self.fall == -1:
            self.y = self.y + 16
            self.fall = self.fall + 1

            if self.fall > 1000:
                self.alive = False

        display.blit(self.image, (self.x, self.y))

    def hit(self, player):
        if player.y > 0:
            self.fall = 0
            pygame.mixer.Sound.play(self.sound)
        else:
            player.fall()
            pygame.mixer.Sound.play(self.bite)

    def can_hit(self, player) -> bool:
        return True
