import os
import ctypes
import pygame
from ui import GameUi, StartMenu, GameOverMenu, PauseMenu
from constant import const
from soundpro import bgm
from player.player_core import Player
from enemy import Enemy
from map import create_map

def initialize_game():
    # DPI対応
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

    # ウィンドウ位置設定
    screen_size = const.get_screen_size()
    if screen_size:
        x = (screen_size[0] - const.SCREEN_WIDTH) // 2
        y = (screen_size[1] - const.SCREEN_HEIGHT) // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
    else:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

    # pygame初期化
    pygame.init()
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman Player and Enemy Test")
    clock = pygame.time.Clock()

    # UI・フォント・メニュー
    next_font = pygame.font.Font(None, const.NEXT_FONT_SIZE)
    ui = GameUi()
    menu = StartMenu(screen)
    go = GameOverMenu(screen)
    pause = PauseMenu(screen)

    # スタートメニュー表示
    menu.draw(screen)

    # BGMとマップ
    stage_bgm = bgm("assets\\bgm\\base2_maou_bgm_healing15.mp3")
    map = create_map()

    if not menu.flg_stage_command:
        map_file = const.MAP_DATA.get(3, next(iter(const.MAP_DATA.values())))
        game_map, original_map = map.load_map(map_file)
    else:
        game_map = map.generate_map(21)
        original_map = [row[:] for row in game_map]

    map_surface = pygame.Surface(screen_size)
    map.draw_map(map_surface, game_map)

    # プレイヤーと敵
    player = Player("assets\\charactor\\conkichi01.png", 0 * const.TILE_SIZE, 0 * const.TILE_SIZE, game_map)
    enemies = Enemy.initialize_enemies(game_map, count=2)

    return {
        "screen": screen,
        "clock": clock,
        "screen_size": screen_size,
        "next_font": next_font,
        "ui": ui,
        "menu": menu,
        "go": go,
        "pause": pause,
        "stage_bgm": stage_bgm,
        "map": map,
        "game_map": game_map,
        "original_map": original_map,
        "map_surface": map_surface,
        "player": player,
        "enemies": enemies
    }