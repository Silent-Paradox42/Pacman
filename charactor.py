"""
キャラクターの基底クラスを定義するモジュール。
画像の読み込み・描画・向き変更など共通処理を提供。
"""
import pygame
from constant import const

class charactor:
    """
    キャラクターの基底クラス。
    プレイヤー・敵などの共通処理（画像管理・描画・向き変更）を持つ。
    """
    def __init__(self, pict=None, x=1, y=1):
        """
        キャラクター画像の読み込み・初期化。
        :param pict: 画像ファイルパス
        :param x: 初期x座標
        :param y: 初期y座標
        """
        self.image = pygame.transform.scale(pygame.image.load(pict), (const.CHAR_SIZE, const.CHAR_SIZE))
        self.x = x
        self.y = y
        self.original_image = self.image.copy()  # 回転・反転前の元画像
        self.current_direction = 'right'  # 現在の向き

    def draw_charactor(self, screen):
        """
        キャラクター画像を画面に描画する。
        :param screen: pygameのSurface
        """
        screen.blit(self.image, (self.x, self.y))

    def update_direction(self, direction):
        """
        キャラクター画像を進行方向に合わせて回転・反転する。
        :param direction: 新しい進行方向
        """
        if direction == self.current_direction:
            return

        img = self.original_image
        if direction == 'up':
            self.image = pygame.transform.rotate(img, 90)
        elif direction == 'down':
            self.image = pygame.transform.rotate(img, 270)
        elif direction == 'left':
            self.image = pygame.transform.flip(img, True, False)
        elif direction == 'right':
            self.image = img.copy()

        self.current_direction = direction
            
