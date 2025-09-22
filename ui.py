import pygame
from player import Player
from map.map import load_map, draw_map
import sys

class GameUi():
    def __init__(self):
        # スコアとライフの初期化(別途用意があるなら削除)
        self.score = 0
        self.lives = 3

    #スコアの加算処理
    def add_score(self, points):
        self.score += points

    #ライフの減算処理
    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    #スコアとライフの描画処理
    def draw(self, screen):
        #font = pygame.font.SysFont("Wide Latin", 20)
        font = pygame.font.SysFont("Snap ITC", 18)
        text = font.render(f"Score: {self.score}    Life : {self.lives}", True, (255, 255, 255))
        screen.blit(text,(10,10))

    #状態リセット処理
    def reset(self):
        self.score = 0
        self.lives = 3

    #ゲームオーバー判定(仮)
    def is_game_over(self):
        return self.lives <= 0
        
#デバッグメイン
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()
    
    game_point = GameUi()
    player = Player("assets\\charactor\\pacman.png", 1 * 32, 1 * 32)

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update([])
        player.draw(screen)
        player.draw_charactor(screen)
        game_point.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()