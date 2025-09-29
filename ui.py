import pygame
from player import Player
from assets.map.map import create_map as map 
from constant import constant as const
import sys
import soundpro

pygame.init()

def add_grahical_prompt(screen,command,font,color=(0,200,0)):
    for i ,com in enumerate(command):   #commandの行数分繰り返し
    #描画設定
        text_surface = font.render(com,True,color)
        #描画の縦位置指定
        y  = screen.get_height() // 2 + i * text_surface.get_height()
        setPosition = (screen.get_width() // 2 - text_surface.get_width() // 2,y)
        #描画処理
        screen.blit(
            text_surface,
            setPosition
        )

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

class PauseMenu():
    def __init__(self, scrsize):
        self.key = None
        self.font = pygame.font.SysFont("yumincho", 72)
        self.small_font = pygame.font.SysFont("yumincho", 36)
        self.subscreen = pygame.surface.Surface((scrsize[0] ,scrsize[1]),pygame.SRCALPHA)
        self.subscreen.fill((0, 0, 50,150))  # 半透明の緑背景

        title_prompt = self.font.render("ぽ～～ず", True, (0, 200, 0))
        self.subscreen.blit(title_prompt, (self.subscreen.get_width() // 2 - title_prompt.get_width() // 2, 100))
        self.opencount = 0
        
        command = ["【Enter】リトライ","【Esc】ぽ～～ず解除","【Q】シャットダウン"]
        add_grahical_prompt(self.subscreen,command,self.small_font)

    def draw(self,screen):
        self.opencount += 1
        screen.blit(self.subscreen,(0,0))
        self.wait_for_start()
    
    def wait_for_start(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q) : 
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    self.key = pygame.K_ESCAPE

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                    self.key = pygame.K_RETURN
            pygame.display.flip()
            pygame.time.Clock().tick(20)  # 60FPSでループ



class StartMenu():
    def __init__(self, scrsize):
        self.font = pygame.font.SysFont("yumincho", 48)
        self.small_font = pygame.font.SysFont("yumincho", 36)
        self.subscreen = pygame.surface.Surface((scrsize[0] ,scrsize[1]),pygame.SRCALPHA)
        
        self.bgm = soundpro.bgm("assets\\bgm\\title_maou_bgm_ethnic13.mp3")
        self.image = pygame.image.load("assets\\title\\titleSample.png")
        
        self.subscreen.fill((0, 0, 50))  # ダークブルー背景
        self.subscreen.blit(self.image, (self.subscreen.get_width() // 2 - self.image.get_width() // 2, 50))
        
        self.command = ["Enterキーでスタート","","※プレイ中【Esc】でpause可能"]
        add_grahical_prompt(self.subscreen,self.command,self.small_font,color=(200,200,200))

        self.flg_stage_command = False

    def draw(self,screen):
        screen.blit(self.subscreen,(0,0))
        self.wait_for_start(screen)

    def wait_for_start(self,screen):
        waiting = True
        self.bgm.play(fade_ms=1000)
        key_history = []
        basetime = pygame.time.get_ticks()
        while waiting:
            #ウィンドウ×ボタンを押下したときの処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.bgm.stop(1000) 
                    pygame.quit()
                    exit()
                #Enterキーを押下したときの処理
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.bgm.stop(1000) 
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if (pygame.time.get_ticks() - basetime) <= const.INPUT_TIME:
                        key_history.append(event.key)
                    elif (pygame.time.get_ticks() - basetime) > const.INPUT_TIME or (len(key_history) > 10):
                        key_history.clear()
                        basetime = pygame.time.get_ticks()

            #print(f"key_history:{key_history}")
            if const.KONAMI_CODE == key_history:
                self.command.append("OPEN RANDOM STAGE")

                self.subscreen.fill((0, 0, 50))  # 背景色で塗りつぶす
                self.subscreen.blit(self.image, (self.subscreen.get_width() // 2 - self.image.get_width() // 2, 50))
                add_grahical_prompt(self.subscreen, self.command, self.small_font, color=(0,200,0))

                screen.blit(self.subscreen,(0,0))

                self.flg_stage_command = True
                key_history.clear()
                basetime = pygame.time.get_ticks()

            pygame.display.flip()
            pygame.time.Clock().tick(20)  # 60FPSでループ


class GameOverMenu():
    def __init__(self, scrsize):
        self.font = pygame.font.SysFont("yumincho", 72)
        self.small_font = pygame.font.SysFont("yumincho", 36)
        self.subscreen = pygame.surface.Surface((scrsize[0] ,scrsize[1]),pygame.SRCALPHA)
        self.subscreen.fill((0, 52, 0,150))  # 半透明の緑背景
        
        self.bgm = soundpro.bgm('assets\\bgm\\GameOver_maou_bgm_8bit20.mp3')
        
        title_prompt = self.font.render("げ～むお～ば～～", True, (0, 200, 0))
        self.subscreen.blit(title_prompt, (self.subscreen.get_width() // 2 - title_prompt.get_width() // 2, 100))
        
        self.command = ["【Enter】リトライ","【Q】シャットダウン"]
        add_grahical_prompt(self.subscreen,self.command,self.small_font,color=(0,200,0))
        

    def draw(self,screen):
        screen.blit(self.subscreen,(0,0))
        self.wait_for_start()
    
    def wait_for_start(self):
        waiting = True
        self.bgm.play(fade_ms=1000)
        while waiting:
            for event in pygame.event.get():
                #ウィンドウ×ボタンもしくはQキーを押下したときの処理
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q) : 
                    self.bgm.stop(1000) 
                    pygame.quit()
                    exit()
                #Enterキーを押下したときの処理
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.bgm.stop(1000) 
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