import pygame

def handle_player_input(event, player, enemies, game_map):
    """プレイヤーの入力を処理する関数"""
    if event.key == pygame.K_LEFT:
        player.set_direction("left")
    elif event.key == pygame.K_RIGHT:
        player.set_direction("right")
    elif event.key == pygame.K_UP:
        player.set_direction("up")
    elif event.key == pygame.K_DOWN:
        player.set_direction("down")
    elif event.key == pygame.K_SPACE:
        player.fire_beam_all_directions(enemies, game_map)
        
def handle_pause(event, pause, screen, player, game_map, original_map, map, map_surface, stage_bgm):
    """ゲームの一時停止を処理する関数"""
    if event.key == pygame.K_ESCAPE:
        pause.draw(screen)
        if pause.key == pygame.K_RETURN:
            player.reset_state()
            player.reset_position()
            game_map[:] = [row[:] for row in original_map]
            map.draw_map(map_surface, game_map)
            stage_bgm.play(-1, 0, 1000)

def handle_events(player, enemies, game_map, original_map, map, map_surface, stage_bgm, pause, screen):
    """全てのイベントを処理する関数"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            handle_player_input(event, player, enemies, game_map)
            handle_pause(event, pause, screen, player, game_map, original_map, map, map_surface, stage_bgm)
    return True