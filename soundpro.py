import pygame

pygame.init()
pygame.mixer.pre_init()
pygame.mixer.init()

class bgm:
    def __init__(self,filepath):
        """BGMの管理クラス"""
        self.filepath = filepath
        self.volume = 0.2
        
    def play(self,loops=-1,start=0.0,fade_ms=0):
        """BGMを再生するメソッド"""
        pygame.mixer.music.stop()  # 先に止める
        pygame.mixer.music.load(self.filepath)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops,start,fade_ms)
        
    def stop(self,fadeout_ms=0):
        """BGMを停止するメソッド"""
        if fadeout_ms>0:
            pygame.mixer.music.fadeout(fadeout_ms)
        else:
            pygame.mixer.music.stop()

    def pause(self):
        """BGMを一時停止するメソッド"""
        pygame.mixer.music.pause()

    def unpause(self):
        """BGMの一時停止を解除するメソッド"""
        pygame.mixer.music.unpause()

    def set_volume(self,volume):
        """BGMの音量を設定するメソッド"""
        if 0.0<=volume<=1.0:
            self.volume = volume
            pygame.mixer.music.set_volume(volume)

class se:
    def __init__(self,filepath):
        """効果音の管理クラス"""
        self.volume = 1.0
        self.sound = pygame.mixer.Sound(filepath)
        self.sound.set_volume(self.volume)

    def play(self,loops=-1,start=0,fade_ms=0):
        """効果音を再生するメソッド"""
        self.sound.play(loops,start,fade_ms)

    def stop(self,fadeout_ms=0):
        """効果音を停止するメソッド"""
        self.sound.fadeout(fadeout_ms)

    def set_volume(self,volume):
        """効果音の音量を設定するメソッド"""
        if 0.0<=volume<=1.0:
            self.volume = volume
            self.sound.set_volume(self.volume)