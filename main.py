import pygame
from player import Player
from map.map import load_map, draw_map
import sys

TILE_SIZE = 32
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

# 仮のマップ（すべて通れる）
#game_map = [[0 for _ in range(SCREEN_WIDTH // TILE_SIZE)] for _ in range(SCREEN_HEIGHT // TILE_SIZE)]
game_map = load_map("map/sample_stage.csv")

# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Player Test")
clock = pygame.time.Clock()

player = Player("assets\\charactor\\pacman.png", 1*TILE_SIZE, 1*TILE_SIZE)
enemy = Player("assets\\charactor\\Blinky.png", 5*TILE_SIZE, 5*TILE_SIZE)

# メインループ
running = True
while running:
    screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_map(screen, game_map)
    player.update(game_map)
    #player.draw(screen)
    player.draw_charactor(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
