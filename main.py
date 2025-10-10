"""メイン処理"""
import pygame
import sys
import ui as Ui
import os
import ctypes
from constant import constant as const
from soundpro import bgm,se as se
from player import Player
from enemy import Enemy
from map import create_map

# DPI対応
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

# 画面サイズ取得
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
taskbar_height = 40

# ウィンドウ位置を左上に固定
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

pygame.init()
screen_size = (screen_width, screen_height - taskbar_height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pacman Player and Enemy Test")
clock = pygame.time.Clock()

# フォント再定義
next_font = pygame.font.Font(None, const.NEXT_FONT_SIZE)

# uiの初期化
ui = Ui.GameUi()
menu = Ui.StartMenu(screen)
go = Ui.GameOverMenu(screen)
pause = Ui.PauseMenu(screen)

menu.draw(screen) # スタートメニューの表示
stage_bgm = bgm("assets\\bgm\\base2_maou_bgm_healing15.mp3") # BGMの読み込み
map = create_map() # マップオブジェクトの作成

# マップデータの読み込みまたは生成
if not menu.flg_stage_command:
    # 通常マップを読み込む
    map_file = const.MAP_DATA.get(90, next(iter(const.MAP_DATA.values())))
    game_map, original_map = map.load_map(map_file)
else:
    # ランダムマップを生成
    game_map = map.generate_map(21)
    original_map = [row[:] for row in game_map]

map_surface = pygame.Surface(screen_size) # マップ描画用Surfaceの作成
map.draw_map(map_surface, game_map) # マップの描画

# プレイヤーと敵キャラの初期化
player = Player("assets\\charactor\\conkichi01.png", 0 * const.TILE_SIZE, 0 * const.TILE_SIZE, game_map) #マップデータを渡す
enemies = Enemy.initialize_enemies(game_map)
next_phase = False
next_timer_start = 0

# メインループ
running = True
stage_bgm.play(-1,0,1000)   # BGM再生
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
            elif event.key == pygame.K_ESCAPE:
                pause.draw(screen)
                if pause.key == pygame.K_RETURN:
                    player.reset_state()
                    player.reset_position()
                    game_map = [row[:] for row in original_map]
                    map.draw_map(map_surface, game_map)
                    stage_bgm.play(-1,0,1000)   # BGM再生
            elif event.key == pygame.K_SPACE:
                player.fire_beam()

    # playerが敵にあたった時の処理と無敵時間調整
    if player.hit_flash:
        now = pygame.time.get_ticks()
        if player.hit_flash_count < 6:
            if (now - player.hit_flash_timer) // 200 % 2 == 0:
                screen.fill((255, 255, 255))  # 白で塗りつぶし
            else:
                screen.blit(map_surface, (0, 0))
                player.draw_charactor(screen)
                for enemy in enemies:
                    enemy.draw(screen)
                ui.draw(
                    screen,
                    score=player.get_score(),
                    lives=player.get_lifes(),
                    charge=player.beam_charge,
                    max_charge=player.beam_charge_max
                )
            if now - player.hit_flash_timer > (player.hit_flash_count + 1) * 200:
                player.hit_flash_count += 1
        else:  # 無敵時間終了
            player.reset_position()
            for enemy in enemies:
                enemy.reset_position(game_map)
            player.beam_charge = 0  # ← チャージをリセット
            player.can_fire_beam = False  # ← 発射可能フラグもリセット（任意）
            player.hit_flash = False
    else:
        # ドットがすべて消えたか判定
        if create_map.all_dots_cleared(game_map):
            if not next_phase:
                next_phase = True
                next_timer_start = pygame.time.get_ticks()
            else:
                elapsed = pygame.time.get_ticks() - next_timer_start
                if elapsed < 5000:
                    # 5秒間「NEXT」表示（ゲーム停止）
                    screen.blit(map_surface, (0, 0))
                    player.draw_charactor(screen)
                    for enemy in enemies:
                        enemy.draw(screen)                        
                    ui.draw(screen, player.get_score(), player.get_lifes())

                    # 「NEXT」テキストを中央に表示
                    text = next_font.render("NEXT", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
                    screen.blit(text, text_rect)
                else:
                    # 5秒経過後にマップとプレイヤーをリセット（スコアは維持）
                    game_map = [row[:] for row in original_map]
                    map.draw_map(map_surface, game_map)
                    player.reset_position()
                    for enemy in enemies:
                        enemy.reset_position(game_map)                        
                    next_phase = False      
        else:
            # 通常描画・更新
            screen.blit(map_surface, (0, 0))                     # 背景描画（キャッシュ）
            player.update(game_map) #毎フレーム呼ばれるプレイヤーの移動処理
            # ドットを取ったときだけマップを再描画
            if player.check_dot_and_clear(game_map):
                map.draw_map(map_surface, game_map)
            player.check_collision_with_enemy(enemies)           # 敵との当たり判定
            player_pos = (player.x, player.y)
            for enemy in enemies:
                enemy.update(game_map, player_pos)               # 敵の移動処理
            player.draw_charactor(screen)                        # プレイヤー描画
            for enemy in enemies:
                enemy.draw(screen)                               # 敵描画
            ui.draw(
                screen,
                score=player.get_score(),
                lives=player.get_lifes(),
                charge=player.beam_charge,
                max_charge=player.beam_charge_max
            )

        #game over判定
        if player.get_lifes() <= 0:
            go.draw(screen)
            player.reset_state()
            player.reset_position()
            game_map = [row[:] for row in original_map]
            map.draw_map(map_surface, game_map)
            enemies = Enemy.initialize_enemies(game_map)
            stage_bgm.play(-1,0,1000)

    # 画面更新
    pygame.display.flip()
    clock.tick(60)# ゲーム終了処理

pygame.quit() # pygameの終了
sys.exit() # プログラムの終了
