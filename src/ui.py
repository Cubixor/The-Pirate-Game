import pygame

import constants as c

BG_PATH = 'resources/ui/bg.png'
BTN_PATH = 'resources/ui/button.png'


class LostUI:
    def __init__(self):
        bg = pygame.image.load(BG_PATH)
        self.bg = pygame.transform.scale(bg, (bg.get_width() * 4, bg.get_height() * 4))
        self.bg_loc = (c.WINDOW[0] // 2 - self.bg.get_width() // 2, c.WINDOW[1] // 2 - self.bg.get_height() // 2)

        font = pygame.font.Font(None, 72)
        self.text = font.render('YOU LOST!', True, (0, 0, 0))
        self.text_loc = (c.WINDOW[0] // 2 - self.text.get_width() // 2, c.WINDOW[1] // 3 - self.text.get_height() // 2)

    def draw(self, screen):
        """
        Draw the lost UI
        :param screen: screen instance
        :return:
        """
        screen.blit(self.bg, self.bg_loc)
        screen.blit(self.text, self.text_loc)

class StartUI:
    def __init__(self):
        bg = pygame.image.load(BG_PATH)
        self.bg = pygame.transform.scale(bg, (bg.get_width() * 4, bg.get_height() * 4))
        self.bg_loc = (c.WINDOW[0] // 2 - self.bg.get_width() // 2, c.WINDOW[1] // 2 - self.bg.get_height() // 2)

        font = pygame.font.Font(None, 34)

        btn = pygame.image.load(BTN_PATH)
        self.button = pygame.transform.scale(btn, (btn.get_width() * 6, btn.get_height() * 6))
        self.button_loc = (c.WINDOW[0] // 2 - self.button.get_width() // 2, c.WINDOW[1] // 2 - self.button.get_height() // 2)
        self.text = font.render('START', True, (0, 0, 0))
        self.text_loc = (c.WINDOW[0] // 2 - self.text.get_width() // 2, c.WINDOW[1] // 2 - self.text.get_height() // 2)

    def draw(self, screen):
            """
            Draw the start UI
            :param screen: screen instance
            :return:
            """
            screen.blit(self.bg, self.bg_loc)
            screen.blit(self.button, self.button_loc)
            screen.blit(self.text, self.text_loc)
