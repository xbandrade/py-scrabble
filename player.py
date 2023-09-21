class Player:
    def __init__(self):
        self.tiles = []
        self.score = 0

    def draw_tiles(self, bag):
        while (bag and len(self.tiles) < 7):
            self.tiles.append(bag.popleft())
