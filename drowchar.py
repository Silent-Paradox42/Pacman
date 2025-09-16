
import pygame

CHAR_SIZE = 20  

# キャラクター画像の読み込み
class charactor:
    def __init__(self, pict, x=1, y=1):
        print(pict)
        self.image = pygame.transform.scale(pygame.image.load(pict), (CHAR_SIZE, CHAR_SIZE))
        self.x = x
        self.y = y
        print(self.image)
        self.original_image = self.image.copy()
        self.current_direction = 'right'
    
    def draw_charactor(self, screen):
        #print(self.image ,self.x,self.y)
        print(screen)
        print(self.image)
        screen.blit(self.image, (self.x, self.y))


    # self.original_image = ...  # 初期画像を保持する変数
    # self.current_direction = ...  # 現在の向きを保持する変数
    def update_direction(self, direction):
        """
        direction: 'up', 'down', 'left', 'right'
        """
        if not hasattr(self, 'original_image'):
            self.original_image = self.image.copy()
            self.current_direction = 'right'

        # 回転・反転が必要な場合のみ処理
        if direction == self.current_direction:
            return

        img = self.original_image
        if direction == 'up':
            self.image = pygame.transform.rotate(img, 90)
        elif direction == 'down':
            self.image = pygame.transform.rotate(img, -90)
        elif direction == 'left':
            self.image = pygame.transform.flip(img, True, False)
        elif direction == 'right':
            self.image = img
            self.current_direction = direction
            
