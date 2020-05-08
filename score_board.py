import pygame
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:
    def __init__(self, ai_settings, screen, stats):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        self.text_color = 30, 30, 30
        self.font = pygame.font.SysFont(None, 48)

        # 当前得分
        self.score_img = None
        self.score_rect = None
        self.prep_score()

        # 最高得分
        self.high_score_img = None
        self.high_score_rect = None
        self.prep_high_score()

        # 游戏等级
        self.level_img = None
        self.level_rect = None
        self.prep_level()

        # 可用飞船显示
        self.ships = None
        self.prep_ships()

    def prep_score(self):
        score = int(round(self.stats.score, -1))
        score_str = '{:,}'.format(score)
        self.score_img = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = '{:,}'.format(high_score)
        self.high_score_img = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_img = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship.rect.width * ship_number
            ship.rect.y = self.score_rect.top
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)
