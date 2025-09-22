import pygame
from player import Player
from map.map import load_map, draw_map
import sys

class GameUi():
    def __init__(self):
        pass

    #スコアとライフの描画処理
    def draw(self, screen, score=0, lives=3):
        #font = pygame.font.SysFont("Wide Latin", 20)
        font = pygame.font.SysFont("Snap ITC", 18)
        text = font.render(f"Score: {score}    Life : {lives}", True, (255, 255, 255))
        screen.blit(text,(10,10))

    #ゲームオーバー判定(仮)
    def is_game_over(self,lives):
        return lives <= 0

class StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("yumincho", 48)
        self.small_font = pygame.font.SysFont("yumincho", 24)

    def draw(self):
        self.screen.fill((0, 0, 50))  # ダークブルー背景
        image = pygame.image.load("assets\\title\\titleSample.png")
        #title = self.font.render("ジョブコン吉ゲーム", True, (255, 255, 255))
        self.screen.blit(image, (self.screen.get_width() // 2 - image.get_width() // 2, 50))
        prompt = self.small_font.render("Enterキーでスタート", True, (200, 200, 200))
        #self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 200))
        self.screen.blit(prompt, (self.screen.get_width() // 2 - prompt.get_width() // 2, 300))
        pygame.display.flip()

    def wait_for_start(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

        
#デバッグメイン
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()
    
    game_point = gameUi()
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