from input import Input
from platform import Platform, Vanish, Moving, Spikes
from monster import Monster
from manager import Manager
from player import Player
from screen import Screen
import math
import pygame
import random

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

pygame.mixer.music.load('resources/sound/music.mp3')
pygame.mixer.music.play(-1)

display = pygame.display.set_mode((Screen.width, Screen.height))
pygame.display.set_caption('Bumpy')
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 48)


bumpyImage = pygame.image.load('resources/img/bumpy-32.png')
backgroundImage = pygame.image.load('resources/img/background.jpg')
userInput = Input()

score = 0
startlevel = pygame.time.get_ticks()

manager = Manager(display)
i = 0
total = 100
lastVanish = False
for m in range(0, total):
    x = 32 * 4 * 1.2 * i + random.random() * 32 * 2
    y = 568 - 32 * 4 * 1.5 * m

    if False:
        pass
    elif random.random() < 0.1:
        platform = Spikes(x, y)
        lastVanish = True
    elif random.random() < 0.3 and lastVanish == False:
        platform = Moving(x, y)
        lastVanish = False
    elif random.random() < 0.3:
        lastVanish = True
        platform = Vanish(x, y)
    else:
        platform = Platform(x, y)
        lastVanish = False

    if i == total:
        platform = Platform(x, y)

    manager.add_gameObject(platform)

    if random.random() < min(0.5, i * 0.1):
        manager.add_gameObject(Monster(0, y - 64))

    if i > 0 and random.random() > 0.5 ** i:
        i = i - 1
    elif i < 5:
        i = i + 1

player = Player()
coordinates = { 'x': 0, 'y': 0 }

p = 0
topOffset = 0
while True:
    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            quit()

        userInput.event(event)

    player.move_x(userInput.test(x=True))

    x = coordinates['x']
    y = coordinates['y']

    if abs(userInput.get_axis(3)) > 0.3 or abs(userInput.get_axis(4)) > 0.3:
        manager.add_bullet(x, y, userInput.get_axis(4), userInput.get_axis(3))

    if y >= Screen.height - 64:
        offset = -64
        if topOffset <= -offset:
            startlevel = pygame.time.get_ticks()
            player.jump()
        else:
            topOffset = topOffset + offset
            manager.move_view(offset)

    player.tick()

    coordinates['x'] = player.x
    coordinates['y'] = min(Screen.height, y + player.y)

    display.fill((0, 0, 0))
    display.blit(backgroundImage, (0, 0))

    top = 200
    offset = top - coordinates['y']
    if offset > 0:
        coordinates['y'] = top
        manager.move_view(offset)
        topOffset = topOffset + offset

    if player.can_jump() and manager.hit_test(coordinates['x'], coordinates['y'], player):
        player.jump()
    manager.draw()

    display.blit(bumpyImage, (coordinates['x'], coordinates['y']))
    ticks = pygame.time.get_ticks() - startlevel

    text = font.render("%s" % int(topOffset / 10 - ticks / 100 + player.score), True, (128, 128, 128))
    display.blit(text, (Screen.width - text.get_width(), 0))

    pygame.display.update()
    clock.tick(60) # FPS
    manager.tick()

pygame.quit()
