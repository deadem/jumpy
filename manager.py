from platform import Platform

class Manager:
    def __init__(self, display):
        self.gameObjects = []
        self.display = display

    def move_view(self, offset):
        for gameObject in self.gameObjects:
            gameObject.y = gameObject.y + offset

    def add_gameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def tick(self):
        self.gameObjects = list(filter(lambda obj: obj.alive, self.gameObjects))

    def draw(self):
        for gameObject in self.gameObjects:
            gameObject.draw(self.display)

    def hit_test(self, x, y, down) -> bool:
        if not down:
            return False

        for gameObject in self.gameObjects:
            if not gameObject.can_hit(down):
                continue

            if x + 32 >= gameObject.x and x <= gameObject.x + gameObject.width:
                if y + 32 >= gameObject.y and y <= gameObject.y + gameObject.height:
                    gameObject.hit(down)
                    return True

        return False
