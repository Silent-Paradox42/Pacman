import pygame
from player import Player as player
import sys

TILE_SIZE = 32
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 仮のマップ（すべて通れる）
game_map = [[0 for _ in range(SCREEN_WIDTH // TILE_SIZE)] for _ in range(SCREEN_HEIGHT // TILE_SIZE)]

# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Player Test")
clock = pygame.time.Clock()

player = player()

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
