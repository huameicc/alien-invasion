
from time import sleep
from time import time
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard
import game_functions as gf


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # gf.create_fleet(ai_settings, screen, ship, aliens)

    stats = GameStats(ai_settings)
    play_button = Button(ai_settings, screen, 'Play')
    sb = ScoreBoard(ai_settings, screen, stats)

    gf.init_game(ai_settings, stats, sb)

    while True:
        t0 = time()
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets)
            gf.update_aliens(ai_settings, aliens)
            # 子弹碰撞外星人
            gf.check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # 外星人碰撞飞船
            gf.check_ship_hit(ai_settings, stats, sb, screen, ship, bullets, aliens)

        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button, sb)
        t = time() - t0
        if t < 0.01:
            sleep(0.01 - t)
        else:
            print(t)


run_game()
