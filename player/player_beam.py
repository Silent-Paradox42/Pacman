import pygame
from constant import const

class PlayerBeamMixin:
    def fire_beam_all_directions(self, enemies, game_map):
        """ 全方向にビームを発射する """
        if not self.can_fire_beam:
            return

        directions = {
            "up": (0, -const.TILE_SIZE),
            "down": (0, const.TILE_SIZE),
            "left": (-const.TILE_SIZE, 0),
            "right": (const.TILE_SIZE, 0)
        }

        beam_range = 5
        px, py = self.x + const.TILE_SIZE // 2, self.y + const.TILE_SIZE // 2
        self.beam_origin = (px, py)
        self.beam_effects.clear()
        self.beam_effect_timer = pygame.time.get_ticks()

        for dx, dy in directions.values():
            for i in range(1, beam_range + 1):
                bx = px + dx * i
                by = py + dy * i

                grid_x = bx // const.TILE_SIZE
                grid_y = by // const.TILE_SIZE

                if not (0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0])):
                    break
                if game_map[grid_y][grid_x] == 1:  # 壁に当たったら止める
                    break

                for enemy in enemies:
                    ex = enemy.x + const.TILE_SIZE // 2
                    ey = enemy.y + const.TILE_SIZE // 2
                    if abs(ex - bx) < const.TILE_SIZE // 2 and abs(ey - by) < const.TILE_SIZE // 2:
                        enemies.remove(enemy)
                        self.score += 100
                        break

                self.beam_effects.append((bx, by))

        self.beam_charge = 0
        self.can_fire_beam = False

    def draw_beam_effects(self, screen):
        """ ビームエフェクトを描画する """
        now = pygame.time.get_ticks()
        if now - self.beam_effect_timer <= self.beam_effect_duration:
            beam_color = (0, 255, 255)
            beam_width = 12
            origin_x, origin_y = self.beam_origin
            for bx, by in self.beam_effects:
                pygame.draw.line(screen, beam_color, (origin_x, origin_y), (bx, by), beam_width)
