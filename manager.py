from platform import Platform
from screen import Screen
import pygame

class Bullet:
    width = 16
    height = 16
    image = pygame.image.load('resources/img/bullet-16.png')
    maxTicks = 200

    def __init__(self, x, y, deltaX, deltaY):
        self.x = x
        self.y = y
        self.deltaX = deltaX * 24
        self.deltaY = deltaY * 24
        self.tickCount = 0
        self.alive = True

    def draw(self, display):
        if not self.alive:
            return

        display.blit(self.image, (self.x, self.y))

    def tick(self):
        if not self.alive:
            return

        self.tickCount = self.tickCount + 1
        self.x = self.x + self.deltaX
        self.y = self.y + self.deltaY

        if self.tickCount > self.maxTicks:
            self.alive = False
        if self.x + self.width < 0 or self.x > Screen.width or self.y + self.height < 0 or self.y > Screen.height:
            self.alive = False

    def can_hit(self, gameObject):
        if self.x + self.width < gameObject.x:
            return False
        if self.x > gameObject.x + gameObject.width:
            return False
        if self.y + self.height < gameObject.y:
            return False
        if self.y > gameObject.y + gameObject.height:
            return False
        return True

    def hit(self, gameObject):
        gameObject.die()

class Manager:
    def __init__(self, display):
        self.gameObjects = []
        self.bullets = []
        self.display = display
        self.lastBullet = pygame.time.get_ticks()

    def move_view(self, offset):
        for gameObject in self.gameObjects:
            gameObject.y = gameObject.y + offset

    def add_gameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def add_bullet(self, x, y, deltaX, deltaY):
        bullet = pygame.time.get_ticks()
        if self.lastBullet + 1000 / 3 < bullet:
            self.lastBullet = bullet
            self.bullets.append(Bullet(x, y, deltaX, deltaY))

    def tick(self):
        self.gameObjects = list(filter(lambda obj: obj.alive, self.gameObjects))
        self.bullets = list(filter(lambda obj: obj.alive, self.bullets))

    def draw(self):
        for bullet in self.bullets:
            bullet.tick()
            bullet.draw(self.display)

        for gameObject in self.gameObjects:
            gameObject.draw(self.display)

    def hit_test(self, x, y, player) -> bool:
        for gameObject in self.gameObjects:
            if gameObject.killable:
                for bullet in self.bullets:
                    if bullet.can_hit(gameObject):
                        bullet.hit(gameObject)

            if not gameObject.can_hit(player):
                continue

            if x + 32 >= gameObject.x and x <= gameObject.x + gameObject.width:
                if y + 32 >= gameObject.y and y <= gameObject.y + gameObject.height:
                    gameObject.hit(player)
                    return True

        return False
