import sys
import pygame
from init_game import initialize_game
from event_handler import handle_events
from game_logic import (
    update_player_and_enemies,
    handle_next_phase,
    add_enemy_if_needed,
    check_game_over
)
from draw_handler import (
    draw_hit_flash,
    draw_next_phase,
    draw_gameplay
)
from map import create_map

def main():
    # オブジェクト変数を各変数に割り振り
    game_data = initialize_game()
    screen = game_data["screen"]
    clock = game_data["clock"]
    screen_size = game_data["screen_size"]
    next_font = game_data["next_font"]
    ui = game_data["ui"]
    go = game_data["go"]
    pause = game_data["pause"]
    stage_bgm = game_data["stage_bgm"]
    map = game_data["map"]
    game_map = game_data["game_map"]
    original_map = game_data["original_map"]
    map_surface = game_data["map_surface"]
    player = game_data["player"]
    enemies = game_data["enemies"]

    next_phase = False
    next_phase_drawn = False
    phase_count = 0
    next_timer_start = 0
    last_enemy_add_time = pygame.time.get_ticks()
    enemy_add_interval = 20000
    stage_bgm.play(-1, 0, 1000)
    running = True

    while running:
        screen.fill((0, 0, 0))
        running = handle_events(player, enemies, game_map, original_map, map, map_surface, stage_bgm, pause, screen)
        now = pygame.time.get_ticks()

        if player.hit_flash:
            if player.hit_flash_count < 6:
                draw_hit_flash(screen, map_surface, player, enemies, ui, now)
                if now - player.hit_flash_timer > (player.hit_flash_count + 1) * 200:
                    player.hit_flash_count += 1
            else:
                player.reset_position()
                for enemy in enemies:
                    enemy.reset_position(game_map)
                player.beam_charge = 0
                player.can_fire_beam = False
                player.hit_flash = False

        elif create_map.all_dots_cleared(game_map) or next_phase:
            """次のステージへ進む処理"""
            if not next_phase:
                phase_count += 1

            next_phase, next_timer_start, phase_finished = handle_next_phase(
                next_phase, next_timer_start,
                game_map, original_map,
                map, map_surface,
                player, enemies
            )

            if next_phase_drawn and pygame.time.get_ticks() - next_timer_start < 5000:
                draw_next_phase(screen, map_surface, player, enemies, ui, next_font, screen_size)
                pygame.display.flip()
                clock.tick(60)
                continue

            if phase_finished:
                next_phase_drawn = False

        else:
            update_player_and_enemies(player, enemies, game_map, map, map_surface)
            last_enemy_add_time = add_enemy_if_needed(enemies, game_map, last_enemy_add_time, enemy_add_interval)
            draw_gameplay(screen, map_surface, player, enemies, ui)

        new_enemies = check_game_over(player, go, screen, game_map, original_map, map, map_surface, stage_bgm)
        if new_enemies is not None:
            enemies = new_enemies

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()