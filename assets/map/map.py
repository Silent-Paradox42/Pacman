
# マップデータの管理・描画・読み込みを行うモジュール

import pygame
import csv
import copy

from constant import constant as const

# マップIDと対応するCSVファイルパスの辞書
MAP_DATA={
    1:'assets/map/stage1.csv',
    2:'assets/map/stage2.csv',
    3:'assets/map/sample_stage3.csv',
    90:'assets/map/pacman_stage.csv',
    91:'assets/map/sample_stage.csv',
}


# タイル画像の読み込み（地面・壁・アイテム）
tile_images = {
    'load': pygame.transform.scale( pygame.image.load("assets/tiles/tuchi.png"),(const.TILE_SIZE,const.TILE_SIZE)),
    'wall': pygame.transform.scale(pygame.image.load("assets/tiles/kabe_black.png"),(const.TILE_SIZE,const.TILE_SIZE)),
    'dot': pygame.transform.scale(pygame.image.load("assets/tiles/item.png"),(const.TILE_SIZE/4,const.TILE_SIZE/4))
}


def load_map(filename):
    """
    CSVファイルからマップデータを読み込む。
    :param filename: マップCSVファイルパス
    :return: 2次元リスト（int型）
    """
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        MAP_DATA = [[int(cell) for cell in row] for row in reader]
        original_map = copy.deepcopy(MAP_DATA)  # オリジナルのマップデータを保存
        return MAP_DATA, original_map

def draw_map(screen, map_data):
    """
    マップデータをもとに画面にタイル画像を描画する。
    :param screen: pygameのSurface
    :param map_data: 2次元リストのマップデータ
    """
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile in [0,2]:
                screen.blit(tile_images['load'], (x * const.TILE_SIZE, y * const.TILE_SIZE))
            if tile == 1:
                screen.blit(tile_images['wall'], (x * const.TILE_SIZE, y * const.TILE_SIZE))
            if tile == 2:
                screen.blit(tile_images['dot'], (x * const.TILE_SIZE + const.TILE_SIZE/2 - const.TILE_SIZE/8, y * const.TILE_SIZE + const.TILE_SIZE/2 - const.TILE_SIZE/8))

def main():
    """
    単体テスト用のメイン処理。マップのみを表示する。
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()

    map_data = load_map(MAP_DATA[0])

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_map(screen, map_data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
