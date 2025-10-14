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

        px, py = self.x + const.TILE_SIZE // 2, self.y + const.TILE_SIZE // 2
        self.beam_origin = (px, py)
        self.beam_effects.clear()
        self.beam_effect_timer = pygame.time.get_ticks()

        for dx, dy in directions.values():
            i = 1
            first_beam = True
            while True:
                bx = px + dx * i
                by = py + dy * i

                grid_x = bx // const.TILE_SIZE
                grid_y = by // const.TILE_SIZE

                if not (0 <= grid_y < len(game_map) and 0 <= grid_x < len(game_map[0])):
                    break
                if game_map[grid_y][grid_x] == 1:
                    break

                for enemy in enemies:
                    ex = enemy.x + const.TILE_SIZE // 2
                    ey = enemy.y + const.TILE_SIZE // 2
                    if abs(ex - bx) < const.TILE_SIZE // 2 and abs(ey - by) < const.TILE_SIZE // 2:
                        enemies.remove(enemy)
                        self.score += 100
                        break

                if first_beam:
                    # 最初のビームの位置を始点にする（キャラの外側）
                    self.beam_effects.append(("origin", (bx, by)))
                    first_beam = False
                else:
                    self.beam_effects.append(("line", (bx, by)))

                i += 1

        self.beam_charge = 0
        self.can_fire_beam = False

    def draw_beam_effects(self, screen):
        """ ビームエフェクトを描画する """
        now = pygame.time.get_ticks()
        if now - self.beam_effect_timer <= self.beam_effect_duration:
            beam_color = (0, 255, 255)
            beam_width = 16
            origin_x, origin_y = None, None
            for kind, (bx, by) in self.beam_effects:
                if kind == "origin":
                    origin_x, origin_y = bx, by
                elif kind == "line" and origin_x is not None:
                    pygame.draw.line(screen, beam_color, (origin_x, origin_y), (bx, by), beam_width)
        else:
            self.beam_effects.clear()