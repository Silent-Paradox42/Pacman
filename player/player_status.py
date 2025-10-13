import pygame
from constant import const

class PlayerStatusMixin:
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

    def lost_life(self):
        """
        ライフを1減らす。
        """
        if self.lifes > 0:
            self.lifes -= 1

    def check_collision_with_enemy(self, enemies):
        """
        敵キャラと衝突したか判定し、衝突したらライフを1減らし無敵状態にする。
        :param enemies: 敵キャラリスト
        """
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
    
