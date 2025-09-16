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

    def is_aligned_to_tile(self):
        margin = 4  # 許容誤差（px）
        return abs((self.x % TILE_SIZE) - TILE_SIZE // 2) < margin and abs((self.y % TILE_SIZE) - TILE_SIZE // 2) < margin

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
        
        if self.is_aligned_to_tile():
            direction = (
                'left' if keys[pygame.K_LEFT] else
                'right' if keys[pygame.K_RIGHT] else
                'up' if keys[pygame.K_UP] else
                'down' if keys[pygame.K_DOWN] else
                None
            )
            if direction:
                self.update_direction(direction)

        if self.can_move_to(new_x, new_y, game_map):
            self.x, self.y = new_x, new_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 10)

    def can_move_to(self, x, y, game_map):
        CHAR_SIZE = TILE_SIZE  # または self.image.get_width() などで取得

        corners = [
            (x, y),  # 左上
            (x + CHAR_SIZE - 1, y),  # 右上
            (x, y + CHAR_SIZE - 1),  # 左下
            (x + CHAR_SIZE - 1, y + CHAR_SIZE - 1)  # 右下
        ]

        for cx, cy in corners:
            grid_x = cx // TILE_SIZE
            grid_y = cy // TILE_SIZE
            if not (0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0])):
                return False
            if game_map[grid_y][grid_x] not in [0, 2]:
                return False

        return True
