import pygame


class Direction:
    x = 1,
    y = 2


class Input:
    state = {Direction.x: 0}
    axis0 = 0
    axis = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    def set_state(self, direction, value):
        self.state[direction] = value

    def move_axis0(self, value):
        axis = self.axis0
        self.axis0 = value
        if abs(value) > 0.3:
            if value > 0.5 and value > axis:
                self.set_state(Direction.x, 1)
            if value < 0 and value < axis:
                self.set_state(Direction.x, -1)
        else:
            self.set_state(Direction.x, 0)

    def move_axis(self, num, value):
        if abs(value) < 0.3:
            value = 0
        self.axis[num] = value

    def move_keys(self, event):
        if event.key == 275:
            self.set_state(Direction.x, 1 if event.type == pygame.KEYDOWN else 0)
        if event.key == 276:
            self.set_state(Direction.x, -1 if event.type == pygame.KEYDOWN else 0)

    def event(self, event):
        if event.type == pygame.JOYAXISMOTION:
            self.move_axis(event.axis, event.value)
            if event.axis == 0:
                self.move_axis0(event.value)

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.move_keys(event)

    def test(self, x=False):
        if x:
            return self.state[Direction.x]

    def get_axis(self, num):
        return self.axis[num]
