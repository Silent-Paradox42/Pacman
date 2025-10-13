import pygame

pygame.init()
pygame.mixer.pre_init()
pygame.mixer.init()
class bgm:
    def __init__(self,filepath):
        self.filepath = filepath
        self.volume = 0.2
        
    def play(self,loops=-1,start=0.0,fade_ms=0):
        pygame.mixer.music.stop()  # 先に止める
        pygame.mixer.music.load(self.filepath)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops,start,fade_ms)
        
    def stop(self,fadeout_ms=0):
        if fadeout_ms>0:
            pygame.mixer.music.fadeout(fadeout_ms)
        else:
            pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()
    def unpause(self):
        pygame.mixer.music.unpause()
    def set_volume(self,volume):
        if 0.0<=volume<=1.0:
            self.volume = volume
            pygame.mixer.music.set_volume(volume)

class se:
    def __init__(self,filepath):
        self.volume = 1.0
        self.sound = pygame.mixer.Sound(filepath)
        self.sound.set_volume(self.volume)

    def play(self,loops=-1,start=0,fade_ms=0):
        self.sound.play(loops,start,fade_ms)

    def stop(self,fadeout_ms=0):
        self.sound.fadeout(fadeout_ms)

    def set_volume(self,volume):
        if 0.0<=volume<=1.0:
            self.volume = volume
            self.sound.set_volume(self.volume)

def main():
    import time
    # pygameの初期化
    pygame.init()
    pygame.mixer.init()
    # MP3ファイルのロード
    sound1 = se("C:\\work\\takimoto\\Coder\\packman\\assets\\bgm\\base_maou_bgm_8bit17.mp3")
    sound2 = se("C:\\work\\takimoto\\Coder\\packman\\assets\\bgm\\GameOver_maou_bgm_8bit20.mp3")
    # 同時に再生
    sound1.play()
    sound2.play()
    # 再生中の時間を待つ
    time.sleep(10)  # 10秒間再生
    # pygameの終了
    pygame.quit()

if __name__ == "__main__":
    main()
