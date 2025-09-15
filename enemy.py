import pygame
import random

class Enemy:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.speed = 2
        self.direction = random.choice(["left", "right", "up", "down"])

    def update(self, game_map):
        # ランダム移動（後でAIに変更）
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # TODO: 壁との当たり判定を追加する（playerと同じように）

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)
