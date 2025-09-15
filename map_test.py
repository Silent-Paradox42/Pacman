import pygame

class Map:
    def __init__(self):
        self.tiles = [
            "####################",
            "#........#.........#",
            "#.####.#.#.#######.#",
            "#..................#",
            "####################"
        ]

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == "#":
                    pygame.draw.rect(screen, (0, 0, 255), (x*32, y*32, 32, 32))
                elif tile == ".":
                    pygame.draw.circle(screen, (255, 255, 255), (x*32+16, y*32+16), 4)

    def is_wall(self, x, y):
        grid_x = x // 32
        grid_y = y // 32
        return self.tiles[grid_y][grid_x] == "#"
