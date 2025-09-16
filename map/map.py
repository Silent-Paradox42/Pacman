#import sys
#print(sys.modules)

import pygame
import csv

TILE_SIZE = 32 #map1マスのサイズ

MAP_DATA={
    0:'map/pacman_stage.csv',
    1:'map/sample_stage.csv',
    2:'map/sample_stage2.csv',
    3:'map/sample_stage3.csv',
}

# タイル画像の読み込み
tile_images = {
    # 
    'load': pygame.transform.scale( pygame.image.load("assets/tiles/tuchi.png"),(TILE_SIZE,TILE_SIZE)),
    'wall': pygame.transform.scale(pygame.image.load("assets/tiles/kabe_black.png"),(TILE_SIZE,TILE_SIZE)),
    'dot': pygame.transform.scale(pygame.image.load("assets/tiles/item.png"),(TILE_SIZE/4,TILE_SIZE/4))
}

# マップ読み込み関数
def load_map(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [[int(cell) for cell in row] for row in reader]

# マップ描画関数
def draw_map(screen, map_data):
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            #print(x,tile,type(x),type(tile))
            #screen.blit(tile_images[tile], (x * TILE_SIZE, y * TILE_SIZE))
            if tile in [0,2]:
                screen.blit(tile_images['load'], (x * TILE_SIZE, y * TILE_SIZE))
            
            if tile == 1:
                screen.blit(tile_images['wall'], (x * TILE_SIZE, y * TILE_SIZE))
            
            if tile == 2:
                screen.blit(tile_images['dot'], (x * TILE_SIZE + TILE_SIZE/2 - TILE_SIZE/8, y * TILE_SIZE + TILE_SIZE/2 - TILE_SIZE/8))

# メイン処理
def main():
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
