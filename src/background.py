import pygame

import constants as c
from animator import Animation

BG_PATH = 'resources/background/BG Image.png'
CLOUD_PATH = 'resources/background/Big Clouds.png'
WATER_PATH = 'resources/background/water'
WATER_REFLEX_PATH = 'resources/background/water_reflex'
WATER_REFLECT_PATH = 'resources/background/water_reflect'
HEALTH_BAR_PATH = 'resources/ui/health.png'


class ScrollingBackground:
    """
    Class for displaying a scrolling background
    along with the health bar
    """

    def __init__(self, dims):
        self.window = dims

        bg_img = pygame.image.load(BG_PATH).convert()
        bg_scaled = pygame.transform.scale(bg_img, dims)
        self.bg_img = bg_scaled

        cloud_img = pygame.image.load(CLOUD_PATH).convert_alpha()
        cloud_scaled = pygame.transform.scale(cloud_img, (cloud_img.get_width() * 3, cloud_img.get_height() * 3))
        self.cloud_img = cloud_scaled

        self.water_anim = Animation({'water': WATER_PATH}, scale=4)
        self.water_reflex = Animation({'water': WATER_REFLEX_PATH}, scale=2)
        self.water_reflect = Animation({'water': WATER_REFLECT_PATH}, scale=4)

        self.speed = c.BG_ANIMATION_SPEED
        self.x1 = 0
        self.x2 = -self.cloud_img.get_width()

        health_img = pygame.image.load(HEALTH_BAR_PATH).convert_alpha()
        health_size = (health_img.get_width() * 4, health_img.get_height() * 4)
        health_img_scaled = pygame.transform.scale(health_img, health_size)
        self.health_bar = health_img_scaled

        self.font = pygame.font.Font(None, 60)

    def update(self):
        """
        Update background images positions and animations
        """
        self.x1 += self.speed
        self.x2 += self.speed
        if self.x1 >= self.cloud_img.get_width():
            self.x1 = self.x2 - self.cloud_img.get_width()
        if self.x2 >= self.cloud_img.get_width():
            self.x2 = self.x1 - self.cloud_img.get_width()

        self.water_anim.update()
        self.water_reflex.update()
        self.water_reflect.update()

    def draw(self, screen, health, score):
        """
        Draw background images
        :param screen: screen instance
        :param health: player health
        """

        screen.blit(self.bg_img, (0, 0))

        screen.blit(self.cloud_img, (self.x1, 180))
        screen.blit(self.cloud_img, (self.x2, 180))
        screen.blit(self.water_reflect.get_image(), (0, 500))
        screen.blit(self.water_reflect.get_image(), (self.window[0] // 2, 500))
        for i in range(0, self.window[0], 384):
            screen.blit(self.water_anim.get_image(), (i, self.window[1] - 64))
            screen.blit(self.water_reflex.get_image(), (i, self.window[1] - 60))
            screen.blit(self.water_reflex.get_image(), (i + 128, self.window[1] - 60))

        self.draw_health_bar(screen, health)
        self.draw_score(screen, score)

    def draw_health_bar(self, screen, health):
        screen.blit(self.health_bar, (20, 20))
        bar_prog = health * 304 / 100
        pygame.draw.rect(screen, pygame.color.Color('Red'), (88, 48, bar_prog, 8))

    def draw_score(self, screen, score):
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        pos = (self.window[0] - score_text.get_width() - 30, score_text.get_height())
        screen.blit(score_text, pos)
