
# 敵キャラクターの挙動を定義するモジュール
import pygame
import random
from drowchar import charactor

TILE_SIZE = 32

class Enemy(charactor):
    """
    敵キャラクタークラス。
    プレイヤーと同様にマップ上を移動し、分岐点でランダムに方向転換する。
    """
    def __init__(self, img="assets\\charactor\\Blinky.png", x=5*TILE_SIZE, y=5*TILE_SIZE):
        """
        敵キャラの初期化。
        :param img: キャラ画像パス
        :param x: 初期x座標
        :param y: 初期y座標
        """
        super().__init__(img, x, y)
        self.x = x
        self.y = y
        self.speed = 2
        # 初期進行方向をランダムに決定
        self.direction = random.choice(["left", "right", "up", "down"])
        self.was_at_branch = False  # 前フレームで分岐点だったか

    def update(self, game_map):
        """
        毎フレーム呼ばれる。敵キャラの移動・方向転換ロジック。
        分岐点ではランダムに方向転換し、壁にぶつかった場合はUターンも許可。
        """
        # 進行可能な方向を調べる
        directions = []
        for d, (dx, dy) in {
            "left": (-self.speed, 0),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "down": (0, self.speed)
        }.items():
            nx, ny = self.x + dx, self.y + dy
            if self.can_move_to(nx, ny, game_map):
                directions.append(d)

        # Uターン方向を除外（進行方向の逆は候補から外す）
        opposite = {"left": "right", "right": "left", "up": "down", "down": "up"}
        candidate_dirs = [d for d in directions if d != opposite.get(self.direction)]

        # 分岐点（進行可能な方向が2つ以上）なら毎回ランダムで方向転換
        if len(directions) >= 2 and candidate_dirs:
            self.direction = random.choice(candidate_dirs)
        elif self.direction not in directions and directions:
            # 進行方向が塞がれている場合はUターンも許可
            self.direction = random.choice(directions)

        # 今の方向に進む（進めなければその場で止まる）
        dx, dy = 0, 0
        if self.direction == "left":
            dx = -self.speed
        elif self.direction == "right":
            dx = self.speed
        elif self.direction == "up":
            dy = -self.speed
        elif self.direction == "down":
            dy = self.speed

        new_x, new_y = self.x + dx, self.y + dy
        if self.can_move_to(new_x, new_y, game_map):
            self.x, self.y = new_x, new_y

        # 進行方向への画像回転・反転
        self.update_direction(self.direction)

    def draw(self, screen):
        """
        画面に敵キャラを描画する。
        """
        self.draw_charactor(screen)

    def can_move_to(self, x, y, game_map):
        CHAR_SIZE = TILE_SIZE

        corners = [
            (x, y),
            (x + CHAR_SIZE - 1, y),
            (x, y + CHAR_SIZE - 1),
            (x + CHAR_SIZE - 1, y + CHAR_SIZE - 1)
        ]

        for cx, cy in corners:
            grid_x = cx // TILE_SIZE
            grid_y = cy // TILE_SIZE
            if not (0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0])):
                return False
            if game_map[grid_y][grid_x] not in [0, 2]:
                return False

        return True
