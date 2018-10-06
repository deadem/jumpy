from platform import Platform

class Manager:
    def __init__(self, display):
        self.platforms = []
        self.display = display

    def add_platform(self, x, y):
        self.platforms.append(Platform(self.display, x, y))

    def draw(self):
        for platform in self.platforms:
            platform.draw()

    def hit_test(self, x, y, down) -> bool:
        if not down:
            return False

        for platform in self.platforms:
            if x + 32 >= platform.x and x <= platform.x + platform.width:
                if y + 32 >= platform.y and y <= platform.y + platform.height:
                    platform.shake()
                    return True

        return False
