import sys
import os
import json
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(ai_settings, stats)
        # 键盘事件
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 发射子弹
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, stats, ship, bullets)
    elif event.key == pygame.K_q:
        quit_game(ai_settings, stats)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # 点击按钮时开始游戏
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        # 重置游戏动态设置
        ai_settings.init_dynamic_settings()

        stats.reset_stats()
        stats.game_active = True
        pygame.mouse.set_visible(False)

        aliens.empty()
        bullets.empty()

        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)

        # 游戏开始时重置计分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()


def update_screen(ai_settings, screen, stats, ship, bullets, aliens, button, sb):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # 绘制所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    # 绘制外星人
    for alien in aliens:
        alien.blitme()
    if not stats.game_active:
        button.draw_button()
    sb.show_score()
    pygame.display.flip()


def fire_bullet(ai_settings, screen, stats, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed and stats.game_active:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(bullets):
    bullets.update()
    # 删除子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def update_aliens(ai_settings, aliens):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """子弹打到外星人"""
    # 子弹外星人碰撞检测
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 计分
    if collisions:
        aliens_hit = set()
        print(collisions)
        aliens_hit.update(*collisions.values())
        stats.score += ai_settings.alien_points * len(aliens_hit)
        sb.prep_score()
        check_high_score(stats, sb)

    if not aliens:
        # 外星人消灭完，重建一批外星人并加快游戏速度
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        bullets.empty()
        # 提升等级
        stats.level += 1
        sb.prep_level()


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.width)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    for row_number in range(number_rows):
        for n in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, n, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - ship_height - 3 * alien_height
    number_rows = int(available_space_y/(2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien.x += 2 * alien.rect.width * alien_number
    alien.rect.x = alien.x
    alien.rect.y += 2 * alien.rect.height * row_number
    aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_ship_hit(ai_settings, stats, sb, screen, ship, bullets, aliens):
    if pygame.sprite.spritecollideany(ship, aliens) or \
            check_aliens_bottom(ai_settings, stats, sb, screen, ship, bullets, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, bullets, aliens)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, bullets, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, bullets, aliens)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, bullets, aliens):
    stats.ships_left -= 1
    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    # 刷新可用飞船
    sb.prep_ships()


def check_high_score(stats, sb):
    """最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def init_game(ai_settings, stats, sb):
    cfg = {}
    if os.path.isfile(ai_settings.config_file):
        with open(ai_settings.config_file, 'r') as f:
            cfg = json.load(f)
    stats.high_score = cfg.get('high_score')
    sb.prep_high_score()


def quit_game(ai_settings, stats):
    cfg = {'high_score' : stats.high_score}
    if not os.path.isdir(os.path.split(ai_settings.config_file)[0]):
        try:
            os.makedirs(os.path.split(ai_settings.config_file)[0])
        except:
            print('error create config file.')
    with open(ai_settings.config_file, 'w') as f:
        json.dump(cfg, f)
    sys.exit()



