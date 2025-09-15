import pygame
import sys

TILE_SIZE = 32
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 仮のマップ（すべて通れる）
game_map = [[0 for _ in range(SCREEN_WIDTH // TILE_SIZE)] for _ in range(SCREEN_HEIGHT // TILE_SIZE)]

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
        if 0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0]):
            return game_map[grid_y][grid_x] == 0
        return False

# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Player Test")
clock = pygame.time.Clock()

player = Player()

# メインループ
running = True
while running:
    screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(game_map)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
