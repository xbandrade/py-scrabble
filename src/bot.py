from src.player import Player


class Bot(Player):
    def __init__(self, id=1):
        super().__init__(id=id, is_bot=True)
