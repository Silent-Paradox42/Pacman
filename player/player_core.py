import pygame
from charactor import charactor
from constant import const
from player.player_movement import PlayerMovementMixin
from player.player_status import PlayerStatusMixin
from player.player_beam import PlayerBeamMixin
from player.player_draw import PlayerDrawMixin

class Player(charactor, PlayerMovementMixin, PlayerStatusMixin, PlayerBeamMixin, PlayerDrawMixin):
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
        self.beam_effects = []  # 発射されたビームの座標リスト（描画用）
        self.beam_effect_timer = 0  # ビーム表示の開始時間
        self.beam_effect_duration = 300  # ミリ秒（0.3秒表示）
        self.beam_origin = (0, 0)  # ビーム発射時のプレイヤー位置

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

    def reset_state(self):
        """
        プレイヤーの状態を初期化。
        """
        self.score = 0
        self.lifes = 3
        self.reset_position()
        self.invincible = False
        self.hit_flash = False
        self.stuck = False
        self.wait_count = 0
        self.beam_charge = 0
        self.can_fire_beam = False

