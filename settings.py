class Settings:
    def __init__(self):
        # 初始化文件
        self.config_file = "config\\alien_invasion.cfg"
        # 屏幕
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # 飞船
        self.ship_speed_factor = 1
        self.ship_limit = 3
        # 子弹
        self.bullet_speed_factor = 1
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 8
        # 外星人
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 30
        self.fleet_direction = 1
        self.alien_points = 50
        # 游戏加速精度
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 2
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

