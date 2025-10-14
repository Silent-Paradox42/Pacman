from constant import const

class PlayerMovementMixin:
    def set_direction(self, direction):
        """
        方向キー入力時に呼ばれる。希望方向をセットし、停止状態なら解除。
        :param direction: 希望する進行方向
        """
        self.next_direction = direction  # 希望方向だけをセット
        # 停止状態なら方向キー入力で解除
        if self.stuck:
            self.stuck = False
            self.wait_count = 0

    def update(self, game_map):
        """
        毎フレーム呼ばれる。プレイヤーの移動・方向転換・Uターン・停止ロジック。
        """
        new_x, new_y = self.x, self.y

        # まず希望方向に進めるなら進行方向を切り替える
        temp_x, temp_y = self.x, self.y
        if self.next_direction == "left":
            temp_x -= self.speed
        elif self.next_direction == "right":
            temp_x += self.speed
        elif self.next_direction == "up":
            temp_y -= self.speed
        elif self.next_direction == "down":
            temp_y += self.speed

        # 完全停止状態なら何もしない（方向キー入力でのみ解除）
        if self.stuck:
            return

        # 壁にぶつかって待機中かどうか
        if self.wait_count > 0:
            self.wait_count += 1
            # 方向キーが押されたら即座に方向転換
            if self.can_move_to(temp_x, temp_y, game_map) and self.direction != self.next_direction:
                self.direction = self.next_direction
                self.update_direction(self.direction)
                self.wait_count = 0
                return
            # 2秒経過（wait_max到達）したら必ず完全停止（stuck）
            if self.wait_count >= self.wait_max:
                self.stuck = True
                self.wait_count = 0
                return

        # 通常時：希望方向に進めるなら進行方向を切り替える
        if self.can_move_to(temp_x, temp_y, game_map):
            if self.direction != self.next_direction:
                self.direction = self.next_direction
                self.update_direction(self.direction)

        # 通常の進行方向で進む
        new_x, new_y = self.x, self.y
        if self.direction == "left":
            new_x -= self.speed
        elif self.direction == "right":
            new_x += self.speed
        elif self.direction == "up":
            new_y -= self.speed
        elif self.direction == "down":
            new_y += self.speed

        if self.can_move_to(new_x, new_y, game_map):
            self.x, self.y = new_x, new_y
            self.wait_count = 0
            
        else:
            # 壁にぶつかったら即座に完全停止
            self.stuck = True
            self.wait_count = 0

    def can_move_to(self, x, y, game_map):
        """
        指定座標(x, y)に移動可能か判定。
        キャラの4隅が通路(0,2)上にあるかチェック。
        :return: Trueなら移動可能
        """
        CHAR_SIZE = const.TILE_SIZE  # または self.image.get_width() などで取得

        corners = [
            (x, y),  # 左上
            (x + CHAR_SIZE - 1, y),  # 右上
            (x, y + CHAR_SIZE - 1),  # 左下
            (x + CHAR_SIZE - 1, y + CHAR_SIZE - 1)  # 右下
        ]

        for cx, cy in corners:
            grid_x = cx // const.TILE_SIZE
            grid_y = cy // const.TILE_SIZE
            if not (0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0])):
                return False
            if game_map[grid_y][grid_x] not in [0, 2]:
                return False

        return True

    def is_aligned_to_tile(self):
        """
        プレイヤーがマス目の中心付近にいるか判定。
        :return: Trueなら中心付近
        """
        margin = 12  # 許容誤差（px）
        return abs((self.x % const.TILE_SIZE) - const.TILE_SIZE // 2) < margin and abs((self.y % const.TILE_SIZE) - const.TILE_SIZE // 2) < margin
