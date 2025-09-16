import pygame
from player import Player
from map.map import MAP_DATA, load_map, draw_map
import sys

TILE_SIZE = 32
SCREEN_WIDTH = TILE_SIZE * 21
SCREEN_HEIGHT = TILE_SIZE * 21

game_map = load_map(MAP_DATA[90])

# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Player Test")
clock = pygame.time.Clock()

player = Player("assets\\charactor\\pacman.png", 1 * TILE_SIZE, 1 * TILE_SIZE, game_map)
#enemy = Player("assets\\charactor\\Blinky.png", 5*TILE_SIZE, 5*TILE_SIZE)

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
