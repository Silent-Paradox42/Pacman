
# ゲームのメイン処理を行うモジュール
import pygame
import sys
from ui import GameUi, StartMenu
from player import Player
from enemy import Enemy
from map.map import MAP_DATA, load_map, draw_map


# 定数定義
TILE_SIZE = 32  # 1マスのサイズ
SCREEN_WIDTH = TILE_SIZE * 21  # 画面幅
SCREEN_HEIGHT = TILE_SIZE * 21  # 画面高さ
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# ドットがすべて消えたか判定する関数
def all_dots_cleared(map_data):
    return all(2 not in row for row in map_data)

# マップ読み込み（MAP_DATA[90] が存在しない場合は最初のマップを使用）
map_file = MAP_DATA.get(91, next(iter(MAP_DATA.values())))
game_map, original_map = load_map(map_file)


# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pacman Player and Enemy Test")
clock = pygame.time.Clock()

# uiの初期化
ui = GameUi()

# スタートメニューの表示
menu = StartMenu(screen)
menu.draw()
menu.wait_for_start()

# プレイヤー初期化
#player = Player("assets\\charactor\\pacman.png", 1 * TILE_SIZE, 1 * TILE_SIZE, game_map)  # プレイヤー生成
player = Player("assets\\charactor\\conkichi01.png", 0 * TILE_SIZE, 0 * TILE_SIZE, game_map) #初期座標テストコード

# --- 敵キャラの自動配置 ---
# 通路マス（2）の座標をリストアップ
enemy_positions = []
for y, row in enumerate(game_map):
    for x, cell in enumerate(row):
        if cell == 2 or cell == 0:
            enemy_positions.append((x, y))

# できるだけ中央付近から4つ選ぶ
center = (len(game_map[0]) // 2, len(game_map) // 2)
enemy_positions.sort(key=lambda pos: (pos[0] - center[0]) ** 2 + (pos[1] - center[1]) ** 2)
enemy_positions = enemy_positions[:4]
enemy  = Enemy("assets\\charactor\\Blinky.png", enemy_positions[0][0] * TILE_SIZE, enemy_positions[0][1] * TILE_SIZE)
enemy2 = Enemy("assets\\charactor\\Blinky.png", enemy_positions[1][0] * TILE_SIZE, enemy_positions[1][1] * TILE_SIZE)
enemy3 = Enemy("assets\\charactor\\Blinky.png", enemy_positions[2][0] * TILE_SIZE, enemy_positions[2][1] * TILE_SIZE)
enemy4 = Enemy("assets\\charactor\\Blinky.png", enemy_positions[3][0] * TILE_SIZE, enemy_positions[3][1] * TILE_SIZE)
flash_count = 0
flash_timer = 0
reset_pending = False

# メインループ
running = True
while running:
    screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                player.set_direction("right")
            elif event.key == pygame.K_UP:
                player.set_direction("up")
            elif event.key == pygame.K_DOWN:
                player.set_direction("down")

    # 👇 ここから明転処理と通常処理を分岐
    if player.hit_flash:
        now = pygame.time.get_ticks()
        if player.hit_flash_count < 6:
            if (now - player.hit_flash_timer) // 200 % 2 == 0:
                screen.fill((255, 255, 255))  # 白で塗りつぶし
            else:
                draw_map(screen, game_map)
                player.draw_charactor(screen)
                enemy.draw(screen)
                enemy2.draw(screen)
                enemy3.draw(screen)
                enemy4.draw(screen)
                ui.draw(screen, player.get_score(), player.get_lifes())
            if now - player.hit_flash_timer > (player.hit_flash_count + 1) * 200:
                player.hit_flash_count += 1
        else:
            player.reset_position()
            player.hit_flash = False
    else:
        # 通常描画・更新
        draw_map(screen, game_map)
        player.update(game_map)
        player.check_dot_and_clear(game_map)
        player.check_collision_with_enemy([enemy, enemy2, enemy3, enemy4])
        player_pos = (player.x, player.y)
        enemy.update(game_map, player_pos)
        enemy2.update(game_map, player_pos)
        enemy3.update(game_map, player_pos)
        enemy4.update(game_map, player_pos)
        player.draw_charactor(screen)
        enemy.draw(screen)
        enemy2.draw(screen)
        enemy3.draw(screen)
        enemy4.draw(screen)
        ui.draw(screen, player.get_score(), player.get_lifes())

    # 画面更新
    pygame.display.flip()
    clock.tick(60)# ゲーム終了処理
pygame.quit()
sys.exit()
