from platform import Platform

class Manager:
    def __init__(self, display):
        self.platforms = []
        self.display = display

    def move_view(self, offset):
        for platform in self.platforms:
            platform.y = platform.y + offset

    def add_platform(self, platform: Platform):
        self.platforms.append(platform)

    def draw(self):
        for platform in self.platforms:
            platform.draw(self.display)

    def hit_test(self, x, y, down) -> bool:
        if not down:
            return False

        for platform in self.platforms:
            if not platform.can_hit():
                continue
            if x + 32 >= platform.x and x <= platform.x + platform.width:
                if y + 32 >= platform.y and y <= platform.y + platform.height:
                    platform.hit()
                    return True

        return False
