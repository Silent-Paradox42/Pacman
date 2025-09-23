import pygame
from player import Player
from assets.map.map import load_map, draw_map
from constant import constant as const
import sys

pygame.init()
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
    def __init__(self, scrsize):
        self.font = pygame.font.SysFont("yumincho", 48)
        self.small_font = pygame.font.SysFont("yumincho", 24)
        self.subscreen = pygame.surface.Surface((scrsize[0] ,scrsize[1]),pygame.SRCALPHA)
        
        self.image = pygame.image.load("assets\\title\\titleSample.png")
        self.prompt = self.small_font.render("Enterキーでスタート", True, (200, 200, 200))
        
        self.subscreen.fill((0, 0, 50))  # ダークブルー背景
        self.subscreen.blit(self.image, (self.subscreen.get_width() // 2 - self.image.get_width() // 2, 50))
        self.subscreen.blit(self.prompt, (self.subscreen.get_width() // 2 - self.prompt.get_width() // 2, 300))
        

    def draw(self,screen):
        screen.blit(self.subscreen,(0,0))
        self.wait_for_start()

    def wait_for_start(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
            pygame.display.flip()
            pygame.time.Clock().tick(20)  # 60FPSでループ

class GameOverMenu():
    def __init__(self, scrsize):
        self.font = pygame.font.SysFont("yumincho", 72)
        self.small_font = pygame.font.SysFont("yumincho", 36)
        self.subscreen = pygame.surface.Surface((scrsize[0] ,scrsize[1]),pygame.SRCALPHA)
        self.subscreen.fill((0, 52, 0,150))  # 半透明の緑背景
        
        title_prompt = self.font.render("げ～むお～ば～～", True, (0, 200, 0))
        self.subscreen.blit(title_prompt, (self.subscreen.get_width() // 2 - title_prompt.get_width() // 2, 50))
        
        command = ["【Enter】リトライ","【Esc】シャットダウン"]
        for i ,com in enumerate(command):   #commandの行数分繰り返し
            #描画設定
            text_surface = self.small_font.render(com,True,(0,200,0))
            #描画の縦位置指定
            y  = self.subscreen.get_height() // 2 + i * text_surface.get_height()
            #描画処理
            self.subscreen.blit(
                text_surface,
                (self.subscreen.get_width() // 2 - text_surface.get_width() // 2,y)
            )

    def draw(self,screen):
        screen.blit(self.subscreen,(0,0))
        self.wait_for_start()

    def wait_for_start(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
            pygame.display.flip()
            pygame.time.Clock().tick(20)  # 60FPSでループ

#デバッグメイン
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()
    go = GameOverMenu(screen)
    
    game_point = GameUi()
    player = Player("assets\\charactor\\pacman.png", 1 * 32, 1 * 32)

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                go.draw()


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