# 敵キャラクターの挙動を定義するモジュール
import pygame
import random
from drowchar import charactor
from constant import constant as const

class Enemy(charactor):
    """
    敵キャラクタークラス。
    プレイヤーと同様にマップ上を移動し、分岐点でランダムに方向転換する。
    """
    def __init__(self, img="assets\\charactor\\black_company.png", x=5*const.CHAR_SIZE, y=5*const.CHAR_SIZE):
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

    def update(self, game_map, player_pos=None):
        """
        毎フレーム呼ばれる。敵キャラの移動・方向転換ロジック。
        分岐点ではランダムに方向転換し、壁にぶつかった場合はUターンも許可。
        """
        # プレイヤーが近い場合は追いかける
        if player_pos is not None:
            px, py = player_pos
            ex, ey = self.x, self.y
            dist = abs((px - ex) // const.CHAR_SIZE) + abs((py - ey) // const.CHAR_SIZE)
            if dist <= 3:
                # 進行可能な方向を調べて最短方向を選ぶ
                directions = []
                for d, (dx, dy) in {
                    "left": (-self.speed, 0),
                    "right": (self.speed, 0),
                    "up": (0, -self.speed),
                    "down": (0, self.speed)
                }.items():
                    nx, ny = self.x + dx, self.y + dy
                    if self.can_move_to(nx, ny, game_map):
                        directions.append((d, nx, ny))
                # 最短距離になる方向を選ぶ
                min_dist = float('inf')
                best_dirs = []
                for d, nx, ny in directions:
                    dval = abs((px - nx) // const.CHAR_SIZE) + abs((py - ny) // const.CHAR_SIZE)
                    if dval < min_dist:
                        min_dist = dval
                        best_dirs = [d]
                    elif dval == min_dist:
                        best_dirs.append(d)
                if best_dirs:
                    # 進行方向の逆は除外
                    opposite = {"left": "right", "right": "left", "up": "down", "down": "up"}
                    candidate_dirs = [d for d in best_dirs if d != opposite.get(self.direction)]
                    if candidate_dirs:
                        self.direction = random.choice(candidate_dirs)
                    else:
                        self.direction = random.choice(best_dirs)
            else:
                # 通常のランダム分岐ロジック
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
                opposite = {"left": "right", "right": "left", "up": "down", "down": "up"}
                candidate_dirs = [d for d in directions if d != opposite.get(self.direction)]
                if len(directions) >= 2 and candidate_dirs:
                    self.direction = random.choice(candidate_dirs)
                elif self.direction not in directions and directions:
                    self.direction = random.choice(directions)
        else:
            # 通常のランダム分岐ロジック
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
            opposite = {"left": "right", "right": "left", "up": "down", "down": "up"}
            candidate_dirs = [d for d in directions if d != opposite.get(self.direction)]
            if len(directions) >= 2 and candidate_dirs:
                self.direction = random.choice(candidate_dirs)
            elif self.direction not in directions and directions:
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
        const.CHAR_SIZE = const.CHAR_SIZE

        corners = [
            (x, y),
            (x + const.CHAR_SIZE - 1, y),
            (x, y + const.CHAR_SIZE - 1),
            (x + const.CHAR_SIZE - 1, y + const.CHAR_SIZE - 1)
        ]

        for cx, cy in corners:
            grid_x = cx // const.CHAR_SIZE
            grid_y = cy // const.CHAR_SIZE
            if not (0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0])):
                return False
            if game_map[grid_y][grid_x] not in [0, 2]:
                return False

        return True
    
    def reset_position(self, game_map):
        """
        敵の位置をマップ上の通路（tile=2 または 0）からランダムに選んで再配置する。
        """
        valid_positions = []
        for y, row in enumerate(game_map):
            for x, tile in enumerate(row):
                if tile in [0, 2]:  # 通路またはドット
                    valid_positions.append((x * const.CHAR_SIZE, y * const.CHAR_SIZE))
        if valid_positions:
            self.x, self.y = random.choice(valid_positions)
