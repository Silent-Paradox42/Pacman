
# マップデータの管理・描画・読み込みを行うモジュール

import pygame
import csv
import copy
import random

from constant import constant as const

# マップIDと対応するCSVファイルパスの辞書

class create_map():
    # タイル画像の読み込み（地面・壁・アイテム）
    def __init__(self):
        self.tile_images = {
            'load': pygame.transform.scale( pygame.image.load("assets/tiles/tuchi.png"),(const.TILE_SIZE,const.TILE_SIZE)),
            'wall': pygame.transform.scale(pygame.image.load("assets/tiles/kabe_black.png"),(const.TILE_SIZE,const.TILE_SIZE)),
            'dot': pygame.transform.scale(pygame.image.load("assets/tiles/item.png"),(const.TILE_SIZE/4,const.TILE_SIZE/4))
        }
        self.filename = ""
        self.map_data = None
        self.original_map = None

    def load_map(self,filename):
        """
        CSVファイルからマップデータを読み込む。
        :param filename: マップCSVファイルパス
        :return: 2次元リスト（int型）
        """
        self.filename = filename
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            MAP_DATA = [[int(cell) for cell in row] for row in reader]
            self.original_map = copy.deepcopy(MAP_DATA)  # オリジナルのマップデータを保存
            self.map_data = MAP_DATA
            self.original_map = [row[:] for row in MAP_DATA]
            return MAP_DATA, self.original_map
        
        return None,None

    def draw_map(self,screen, map_data):
        """
        マップデータをもとに画面にタイル画像を描画する。
        :param screen: pygameのSurface
        :param map_data: 2次元リストのマップデータ
        """
        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile in [0,2]:
                    screen.blit(self.tile_images['load'], (x * const.TILE_SIZE, y * const.TILE_SIZE))
                if tile == 1:
                    screen.blit(self.tile_images['wall'], (x * const.TILE_SIZE, y * const.TILE_SIZE))
                if tile == 2:
                    screen.blit(self.tile_images['dot'], (x * const.TILE_SIZE + const.TILE_SIZE/2 - const.TILE_SIZE/8, y * const.TILE_SIZE + const.TILE_SIZE/2 - const.TILE_SIZE/8))

    #自動マップ生成機能
    def generate_map(self,size):
        maze = [[1 for _ in range(size)] for _ in range(size)]

        # Initialize all inner cells as walls
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                maze[y][x] = 1

        # Carve paths using randomized Prim's algorithm
        def neighbors(cx, cy):
            dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            result = []
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < size - 1 and 1 <= ny < size - 1:
                    result.append((nx, ny))
            return result

        def adjacent_paths(x, y):
            count = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size and maze[ny][nx] != 1:
                    count += 1
            return count

        start_x, start_y = 1, 1
        maze[start_y][start_x] = 0
        walls = [(start_x + dx, start_y + dy, start_x, start_y) for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)] if 1 <= start_x + dx < size - 1 and 1 <= start_y + dy < size - 1]

        while walls:
            wx, wy, px, py = walls.pop(random.randint(0, len(walls) - 1))
            if maze[wy][wx] == 1:
                maze[wy][wx] = 0
                maze[(wy + py) // 2][(wx + px) // 2] = 0
                for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nx, ny = wx + dx, wy + dy
                    if 1 <= nx < size - 1 and 1 <= ny < size - 1 and maze[ny][nx] == 1:
                        walls.append((nx, ny, wx, wy))

        # Ensure all path cells have at least two adjacent paths
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                if maze[y][x] == 0 and adjacent_paths(x, y) < 2:
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = x + dx, y + dy
                        if 1 <= nx < size - 1 and 1 <= ny < size - 1 and maze[ny][nx] == 1:
                            maze[ny][nx] = 0
                            if adjacent_paths(x, y) >= 2:
                                break

        # Convert all path cells to energy paths (value 2)
        for y in range(size):
            for x in range(size):
                if maze[y][x] == 0:
                    maze[y][x] = 2
        self.increase_wall_density(maze)
        return maze
    
    # 迷路生成後に壁の割合を調整
    def increase_wall_density(self,maze, target_wall_ratio=0.5):
        total_cells = len(maze) * len(maze[0])
        current_walls = sum(cell == 1 for row in maze for cell in row)
        target_walls = int(total_cells * target_wall_ratio)

        # ランダムに道を壁に変える（ただし連結性を維持）
        path_cells = [(y, x) for y in range(1, len(maze)-1) for x in range(1, len(maze[0])-1) if maze[y][x] == 2]
        random.shuffle(path_cells)

        for y, x in path_cells:
            if current_walls >= target_walls:
                break
            # 仮に壁にしてみる
            maze[y][x] = 1
            if not self.is_fully_connected(maze):  # 連結性チェック（DFSなど）
                maze[y][x] = 2  # 戻す
            else:
                current_walls += 1
    # 連結性チェック（DFSなど）
    def is_fully_connected(self, maze):
        visited = [[False for _ in row] for row in maze]
        height, width = len(maze), len(maze[0])

        # 最初の道を探す
        for y in range(height):
            for x in range(width):
                if maze[y][x] == 2:
                    start = (y, x)
                    break
            else:
                continue
            break

        # DFSで探索
        stack = [start]
        visited[start[0]][start[1]] = True
        while stack:
            cy, cx = stack.pop()
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < height and 0 <= nx < width and maze[ny][nx] == 2 and not visited[ny][nx]:
                    visited[ny][nx] = True
                    stack.append((ny, nx))

        # すべての道が訪問されたか確認
        for y in range(height):
            for x in range(width):
                if maze[y][x] == 2 and not visited[y][x]:
                    return False
        return True


def main():
    """
    単体テスト用のメイン処理。マップのみを表示する。
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()

    map_data = create_map.load_map(const.MAP_DATA[0])

    running = True
    while running:
        screen.fill((0, 0, 0))
        create_map.ldraw_map(screen, map_data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
