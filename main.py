import pygame
import sys
from player import Player
from enemy import Enemy
from map.map import MAP_DATA, load_map, draw_map

# 定数定義
TILE_SIZE = 32
SCREEN_WIDTH = TILE_SIZE * 21
SCREEN_HEIGHT = TILE_SIZE * 21

# マップ読み込み（MAP_DATA[90] が存在しない場合は最初のマップを使用）
map_file = MAP_DATA.get(90, next(iter(MAP_DATA.values())))
game_map = load_map(map_file)

# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Player and Enemy Test")
clock = pygame.time.Clock()

# プレイヤーと敵の初期化
player = Player("assets\\charactor\\pacman.png", 1 * TILE_SIZE, 1 * TILE_SIZE, game_map)
enemy = Enemy("assets\\charactor\\Blinky.png", 5 * TILE_SIZE, 5 * TILE_SIZE)
enemy2 = Enemy("assets\\charactor\\Blinky.png", 5 * TILE_SIZE, 5 * TILE_SIZE)
enemy3 = Enemy("assets\\charactor\\Blinky.png", 5 * TILE_SIZE, 5 * TILE_SIZE)

# メインループ
running = True
while running:
    screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # マップ描画
    draw_map(screen, game_map)

    # プレイヤーと敵の更新
    player.update(game_map)
    enemy.update(game_map)
    enemy2.update(game_map)
    enemy3.update(game_map)

    # 描画
    player.draw_charactor(screen)
    enemy.draw(screen)
    enemy2.draw(screen)
    enemy3.draw(screen)

    # 画面更新
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
