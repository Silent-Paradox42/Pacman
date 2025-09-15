class GameState:
    def __init__(self):
        self.score = 0
        self.lives = 3

    def add_score(self, points):
        self.score += points

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            return "game_over"
        return "continue"
