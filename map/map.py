#import sys
#print(sys.modules)

import pygame
import csv

TILE_SIZE = 30

# タイル画像の読み込み
tile_images = {
    # 
    0: pygame.transform.scale( pygame.image.load("assets/tiles/tuchi.png"),(TILE_SIZE,TILE_SIZE)),
    1: pygame.transform.scale(pygame.image.load("assets/tiles/kabe_black.png"),(TILE_SIZE,TILE_SIZE)),
    2: pygame.transform.scale(pygame.image.load("assets/tiles/item.png"),(TILE_SIZE,TILE_SIZE))
}
""" TILE_SIZE = 5  # 1マスのサイズを5pxに設定

tile_images = {
    0: pygame.image.load("assets/tiles/dot.png"),
    1: pygame.image.load("assets/tiles/wall.png"),
    2: pygame.image.load("assets/tiles/power_dot.png")
}
 """


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
            screen.blit(tile_images[tile], (x * TILE_SIZE, y * TILE_SIZE))


# メイン処理
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()

    map_data = load_map("map/pacman_narrow_path.csv")

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
