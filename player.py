import pygame
from drowchar import charactor as character
TILE_SIZE = 32  # マップの1マスのサイズ

class Player(character):
    def __init__(self, img="assets\\charactor\\Trollman.png", x=1, y=1, game_map=None):
        super().__init__(img, x, y)
        self.x = x
        self.y = y
        self.speed = 2

        # 初期位置が壁なら安全な位置に移動
        if game_map and not self.can_move_to(x, y, game_map):
            print("⚠️ 初期位置が壁です。安全な位置に移動します。")
            self.x = 2 * TILE_SIZE
            self.y = 2 * TILE_SIZE

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
        if 0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0]):
            return game_map[grid_y][grid_x] in [0, 2]
        return False
    
