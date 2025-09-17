
# ゲームのメイン処理を行うモジュール
import pygame
import sys
from player import Player
from enemy import Enemy
from map.map import MAP_DATA, load_map, draw_map


# 定数定義
TILE_SIZE = 32  # 1マスのサイズ
SCREEN_WIDTH = TILE_SIZE * 21  # 画面幅
SCREEN_HEIGHT = TILE_SIZE * 21  # 画面高さ


# マップ読み込み（MAP_DATA[90] が存在しない場合は最初のマップを使用）
map_file = MAP_DATA.get(90, next(iter(MAP_DATA.values())))
game_map = load_map(map_file)


# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Player and Enemy Test")
clock = pygame.time.Clock()

# プレイヤー初期化
#player = Player("assets\\charactor\\pacman.png", 1 * TILE_SIZE, 1 * TILE_SIZE, game_map)  # プレイヤー生成
player = Player("assets\\charactor\\pacman.png", 0 * TILE_SIZE, 0 * TILE_SIZE, game_map) #初期座標テストコード

# --- 敵キャラの自動配置 ---
# 通路マス（2）の座標をリストアップ
enemy_positions = []
for y, row in enumerate(game_map):
    for x, cell in enumerate(row):
        if cell == 2:
            enemy_positions.append((x, y))
# できるだけ中央付近から4つ選ぶ
center = (len(game_map[0]) // 2, len(game_map) // 2)
enemy_positions.sort(key=lambda pos: (pos[0] - center[0]) ** 2 + (pos[1] - center[1]) ** 2)
enemy_positions = enemy_positions[:4]
enemy  = Enemy("assets\\charactor\\Blinky.png", enemy_positions[0][0] * TILE_SIZE, enemy_positions[0][1] * TILE_SIZE)
enemy2 = Enemy("assets\\charactor\\Blinky.png", enemy_positions[1][0] * TILE_SIZE, enemy_positions[1][1] * TILE_SIZE)
enemy3 = Enemy("assets\\charactor\\Blinky.png", enemy_positions[2][0] * TILE_SIZE, enemy_positions[2][1] * TILE_SIZE)
enemy4 = Enemy("assets\\charactor\\Blinky.png", enemy_positions[3][0] * TILE_SIZE, enemy_positions[3][1] * TILE_SIZE)

# メインループ
running = True
while running:
    screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし

    # イベント処理（ウィンドウの×ボタンやキー入力）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 方向キー入力でプレイヤーの進行方向を変更
            if event.key == pygame.K_LEFT:
                player.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                player.set_direction("right")
            elif event.key == pygame.K_UP:
                player.set_direction("up")
            elif event.key == pygame.K_DOWN:
                player.set_direction("down")

    # マップ描画
    draw_map(screen, game_map)

    # プレイヤーと敵の状態更新
    player.update(game_map)
    player_pos = (player.x, player.y)
    enemy.update(game_map, player_pos)
    enemy2.update(game_map, player_pos)
    enemy3.update(game_map, player_pos)
    enemy4.update(game_map, player_pos)

    # キャラクター描画
    player.draw_charactor(screen)
    enemy.draw(screen)
    enemy2.draw(screen)
    enemy3.draw(screen)
    enemy4.draw(screen)

    # 画面更新
    pygame.display.flip()
    clock.tick(60)  # 60FPSでループ

# ゲーム終了処理
pygame.quit()
sys.exit()
