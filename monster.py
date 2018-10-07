import pygame


class Monster:
    width = 64
    height = 64
    sound = False
    image = pygame.image.load('resources/img/monster.png')

    def __init__(self, x, y, maxX):
        self.x = x
        self.y = y
        self.sound = pygame.mixer.Sound('resources/sound/monster-hit.wav')
        self.fall = -1

    def draw(self, display):
        if not self.fall == -1:
            self.y = self.y + 16

        display.blit(self.image, (self.x, self.y))

    def hit(self, down: bool):
        self.fall = 0
        pygame.mixer.Sound.play(self.sound)

    def can_hit(self, down: bool) -> bool:
        return True
