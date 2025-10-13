
def draw_hit_flash(screen, map_surface, player, enemies, ui, now):
    """プレイヤーがダメージを受けた際の点滅エフェクトを描画する関数"""
    if (now - player.hit_flash_timer) // 200 % 2 == 0:
        screen.fill((255, 255, 255))  # 白で塗りつぶし
    else:
        screen.blit(map_surface, (0, 0))
        player.draw_charactor(screen)
        player.draw_beam_effects(screen)
        for enemy in enemies:
            enemy.draw(screen)
        draw_ui(screen, ui, player)

def draw_next_phase(screen, map_surface, player, enemies, ui, next_font, screen_size):
    """次のステージに進む際の「NEXT」表示を描画する関数"""
    screen.blit(map_surface, (0, 0))
    player.draw_charactor(screen)
    player.draw_beam_effects(screen)
    for enemy in enemies:
        enemy.draw(screen)
    draw_ui(screen, ui, player)

    # 最後にテキストを描画（最前面に表示される）
    text = next_font.render("NEXT", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
    screen.blit(text, text_rect)

def draw_gameplay(screen, map_surface, player, enemies, ui):
    """ゲームプレイ中の描画を行う関数"""
    screen.blit(map_surface, (0, 0))
    player.draw_charactor(screen)
    player.draw_beam_effects(screen)
    for enemy in enemies:
        enemy.draw(screen)
    draw_ui(screen, ui, player)

def draw_ui(screen, ui, player):
    """UIの描画を行う関数"""
    ui.draw(
        screen,
        score=player.get_score(),
        lives=player.get_lifes(),
        charge=player.beam_charge,
        max_charge=player.beam_charge_max
    )