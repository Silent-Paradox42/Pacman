"""プレイヤークラスモジュール"""
import pygame
from drowchar import charactor
from constant import const

class Player(charactor):
    """
    プレイヤーキャラクタークラス。
    方向キー入力や壁衝突時のUターン、停止などの挙動を管理する。
    """
    def __init__(self, img=None, x=1, y=1, game_map=None):
        """
        プレイヤーの初期化。
        :param img: キャラ画像パス
        :param x: 初期x座標
        :param y: 初期y座標
        :param game_map: マップデータ
        :param lifes: 初期ライフ数
        :param score: 初期スコア
        """
        self.img = img # キャラ画像パス

        # 画像が指定されていない場合はデフォルトの赤い四角を使用
        if img:
            self.image = pygame.image.load(img).convert_alpha()
        else:
            self.image = pygame.Surface((const.TILE_SIZE, const.TILE_SIZE))
            self.image.fill((255, 0, 0))
        
        super().__init__(img, x, y) # 親クラスの初期化     
        self.speed = 2 # 移動速度（px/フレーム）
        self.direction = "right"  # 現在の進行方向
        self.next_direction = "right"  # 希望方向（キー入力でセット）
        self.wait_count = 0  # 壁にぶつかった時の待機カウンタ
        self.wait_max = 10   # 何フレーム待つか（調整可）
        self.stuck = False   # 完全停止状態かどうか
        self.score = 0       # スコア
        self.lifes = 3       # ライフ数
        self.x = x * const.TILE_SIZE # 画面上のピクセル座標に変換
        self.y = y * const.TILE_SIZE # 画面上のピクセル座標に変換
        self.start_x = self.x # 初期位置を保存
        self.start_y = self.y # 初期位置を保存
        self.invincible = False # 無敵状態かどうか
        self.invincible_timer = 0 # 無敵状態のタイマー
        self.invincible_duration = 2000  # ミリ秒（2秒間無敵）
        self.hit_flash = False # ダメージを受けた際の点滅状態かどうか
        self.hit_flash_timer = 0 # 点滅状態のタイマー
        self.hit_flash_count = 0 # 点滅回数カウンタ
        self.beam_charge = 0              # 現在のチャージ量
        self.beam_charge_max = 100        # 最大チャージ量
        self.can_fire_beam = False        # 発射可能かどうか

        # マップ外に初期位置がある場合、マップ内の最初の通路マスに移動
        if game_map and not self.can_move_to(self.x, self.y, game_map):
            import tkinter
            root = tkinter.Tk()
            root.withdraw()
            root.destroy()
            found = False
            # マップ内の最初の通路マス(0または2)を探す
            for gy, row in enumerate(game_map):
                # 各行を走査
                for gx, cell in enumerate(row):
                    # 通路マスを発見したらそこに移動
                    if cell in [0, 2]:
                        self.x = gx * const.TILE_SIZE
                        self.y = gy * const.TILE_SIZE
                        self.start_x = self.x
                        self.start_y = self.y
                        found = True
                        break
                # 外側のループも抜ける
                if found:
                    break

        self.update_direction(self.direction)

    def is_aligned_to_tile(self):
        """
        プレイヤーがマス目の中心付近にいるか判定。
        :return: Trueなら中心付近
        """
        margin = 12  # 許容誤差（px）
        return abs((self.x % const.TILE_SIZE) - const.TILE_SIZE // 2) < margin and abs((self.y % const.TILE_SIZE) - const.TILE_SIZE // 2) < margin

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

    def draw(self, screen):
        """
        プレイヤーキャラを画面に描画する。
        """
        self.draw_charactor(screen)

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

    def check_dot_and_clear(self, game_map):
        """プレイヤーがドットを取ったか判定し、取ったら消す。スコア加算とチャージ加算。
        :param game_map: マップデータ"""
        tile_x = self.x // const.TILE_SIZE
        tile_y = self.y // const.TILE_SIZE
        if 0 <= tile_y < len(game_map) and 0 <= tile_x < len(game_map[0]):
            if game_map[tile_y][tile_x] == 2:
                game_map[tile_y][tile_x] = 0
                self.score += 10  # スコア加算

                # チャージ加算処理
                self.beam_charge = min(self.beam_charge + 10, self.beam_charge_max)
                if self.beam_charge >= self.beam_charge_max:
                    self.can_fire_beam = True

                return True
        return False
    
    def reset_position(self):
        """
        プレイヤーを初期位置にリセット。
        """
        self.x = self.start_x # 初期位置にリセット
        self.y = self.start_y # 初期位置にリセット
        self.stuck = False
        self.wait_count = 0
        self.direction = "right"  # 現在の進行方向
        self.next_direction = "right"  # 希望方向（キー入力でセット）

    def get_score(self):
        """
        現在のスコアを取得。
        :return: スコア
        """
        return self.score
    
    def get_lifes(self):
        """
        現在のライフを取得。
        :return: ライフ
        """
        return self.lifes
    def add_score(self, points):
        """
        スコアを加算。
        """
        self.score += points

    def lost_life(self):
        """
        ライフを1減らす。
        """
        if self.lifes > 0:
            self.lifes -= 1
    
    # プレイヤーが敵と衝突したか判定し、衝突したらライフを減らす
    def check_collision_with_enemy(self, enemies):
        if self.invincible or self.hit_flash:
            now = pygame.time.get_ticks()
            if self.invincible and now - self.invincible_timer >= self.invincible_duration:
                self.invincible = False
            return

        for enemy in enemies:
            dx = abs(self.x - enemy.x)
            dy = abs(self.y - enemy.y)
            if dx < const.TILE_SIZE // 2 and dy < const.TILE_SIZE // 2:
                self.lost_life()
                self.invincible = True
                self.invincible_timer = pygame.time.get_ticks()
                self.hit_flash = True
                self.hit_flash_timer = pygame.time.get_ticks()
                self.hit_flash_count = 0
                break

    def fire_beam(self):
        if self.can_fire_beam:
            print("ビーム発射！")  # 実際の処理は後で追加
            self.beam_charge = 0
            self.can_fire_beam = False

    def reset_state(self):
        self.score = 0
        self.lifes = 3
        self.reset_position()
        self.invincible = False
        self.hit_flash = False
        self.stuck = False
        self.wait_count = 0
        self.beam_charge = 0
        self.can_fire_beam = False
