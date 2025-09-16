import pygame
import random
from drowchar import charactor

TILE_SIZE = 32

class Enemy(charactor):
    def __init__(self, img="assets\\charactor\\Blinky.png", x=5*TILE_SIZE, y=5*TILE_SIZE):
        super().__init__(img, x, y)
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = random.choice(["left", "right", "up", "down"])

    def update(self, game_map):
        new_x, new_y = self.x, self.y

        if self.direction == "left":
            new_x -= self.speed
        elif self.direction == "right":
            new_x += self.speed
        elif self.direction == "up":
            new_y -= self.speed
        elif self.direction == "down":
            new_y += self.speed

        if self.can_move_to(new_x, new_y, game_map):
            self.x, self.y = new_x, new_y
        else:
            # 壁にぶつかったら方向をランダムに変更
            self.direction = random.choice(["left", "right", "up", "down"])

    def draw(self, screen):
        self.draw_charactor(screen)

    def can_move_to(self, x, y, game_map):
        CHAR_SIZE = TILE_SIZE

        corners = [
            (x, y),
            (x + CHAR_SIZE - 1, y),
            (x, y + CHAR_SIZE - 1),
            (x + CHAR_SIZE - 1, y + CHAR_SIZE - 1)
        ]

        for cx, cy in corners:
            grid_x = cx // TILE_SIZE
            grid_y = cy // TILE_SIZE
            if not (0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0])):
                return False
            if game_map[grid_y][grid_x] not in [0, 2]:
                return False

        return True
