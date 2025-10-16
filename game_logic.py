import pygame
from enemy import Enemy

def update_player_and_enemies(player, enemies, game_map, map, map_surface):
    """プレイヤーと敵キャラクターの位置更新を行う関数"""
    player.update(game_map)
    if player.check_dot_and_clear(game_map):
        map.draw_map(map_surface, game_map)
    player.check_collision_with_enemy(enemies)
    player_pos = (player.x, player.y)
    for enemy in enemies:
        enemy.update(game_map, player_pos)

def handle_next_phase(next_phase, next_timer_start, game_map, original_map, map, map_surface, player, enemies):
    """次のステージに進む処理を行う関数"""
    if not next_phase:
        return True, pygame.time.get_ticks(), False

    elapsed = pygame.time.get_ticks() - next_timer_start
    if elapsed >= 5000:
        game_map[:] = [row[:] for row in original_map]
        map.draw_map(map_surface, game_map)
        player.reset_position()
        for enemy in enemies:
            enemy.reset_position(game_map)
        return False, 0, True  # フェーズ終了
    return next_phase, next_timer_start, False

def add_enemy_if_needed(enemies, game_map, last_enemy_add_time, enemy_add_interval):
    """一定時間ごとに新しい敵キャラクターを追加する関数"""
    now = pygame.time.get_ticks()
    if now - last_enemy_add_time >= enemy_add_interval:
        new_enemy = Enemy()
        new_enemy.reset_position(game_map)
        enemies.append(new_enemy)
        return now
    return last_enemy_add_time

def check_game_over(player, go, screen, game_map, original_map, map, map_surface, stage_bgm):
    """ゲームオーバー時の処理を行う関数"""
    if player.get_lifes() <= 0:
        go.draw(screen)
        player.reset_state()
        player.reset_position()
        game_map[:] = [row[:] for row in original_map]
        map.draw_map(map_surface, game_map)
        enemies = Enemy.initialize_enemies(game_map)
        stage_bgm.play(-1, 0, 1000)
        return enemies
    return None