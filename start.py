import pygame

pygame.init()

resolution = { 'width': 800, 'height': 600 }

display = pygame.display.set_mode((resolution['width'],resolution['height']))
pygame.display.set_caption('Bumpy')
clock = pygame.time.Clock()

bumpyImage = pygame.image.load('resources/img/bumpy-32.png')
platformImage = pygame.image.load('resources/img/platform-32.png')

joystick = pygame.joystick.Joystick(0)
joystick.init()

class State:
    x = 0
    y = 0
    ticks = 0
    lastY = 0

    def updateX(self, value):
        if abs(value) < 0.3:
            self.x = 0
        elif value > 0.5:
            self.x = 1
        elif value < -0.5:
            self.x = -1

    def updateY(self):
        ticks = pygame.time.get_ticks() / 100
        self.y = self.lastY + (9.8 * (self.ticks - ticks) ** 2) / 4
        if self.y > 20:
            self.y = 20
        # self.ticks = ticks

    def jump(self):
        self.lastY = -20
        self.ticks = pygame.time.get_ticks() / 100

state = State()
coordinates = { 'x': 400, 'y': 0 }

quit = False
while not quit:
    for event in pygame.event.get():
        quit = quit | event.type == pygame.QUIT
        print(event)

        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                state.updateX(event.value)
            # if event.axis == 1:
            #     coordinates['y'] = coordinates['y'] + event.value * 10

    x = coordinates['x']
    y = coordinates['y']

    if y > 534:
        state.jump()

    if (x > 32 * 4) and (x < 32 * 4 + 32 * 4) and (y > 568 - 32 * 5) and (y < 568 - 32 * 4) and (state.y > 0):
        state.jump()

    state.updateY()

    coordinates['x'] = x + state.x * 10
    coordinates['y'] = min(535, y + state.y)

    display.fill((0, 0, 0))
    display.blit(bumpyImage, (coordinates['x'], coordinates['y']))

    display.blit(platformImage, (0, 568))

    display.blit(platformImage, (32 * 4, 568 - 32 * 4))

    pygame.display.update()
    clock.tick(60) # FPS

pygame.quit()
