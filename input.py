import pygame


class Direction:
    x = 1,
    y = 2


class Input:
    state = {Direction.x: 0}
    axis = [0]

    def __init__(self):
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    def set_state(self, direction, value):
        self.state[direction] = value

    def move_axis0(self, value):
        axis = self.axis[0]
        self.axis[0] = value
        if abs(value) > 0.3:
            if value > 0.5 and value > axis:
                self.set_state(Direction.x, 1)
            if value < 0 and value < axis:
                self.set_state(Direction.x, -1)
        else:
            self.set_state(Direction.x, 0)

    def event(self, event):
        if event.type == pygame.JOYAXISMOTION and event.axis == 0:
            self.move_axis0(event.value)

    def test(self, x=False):
        if x:
            return self.state[Direction.x]
