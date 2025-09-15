import pygame

TILE_SIZE = 32  # マップの1マスのサイズ（仮）

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.speed = 2

    def update(self, game_map):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y

        if keys[pygame.K_LEFT]:
            new_x -= self.speed
        elif keys[pygame.K_RIGHT]:
            new_x += self.speed
        elif keys[pygame.K_UP]:
            new_y -= self.speed
        elif keys[pygame.K_DOWN]:
            new_y += self.speed

        if self.can_move_to(new_x, new_y, game_map):
            self.x, self.y = new_x, new_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 10)

    def can_move_to(self, x, y, game_map):
        grid_x = x // TILE_SIZE
        grid_y = y // TILE_SIZE
        return game_map[grid_y][grid_x] == 0  # 0なら通れる
