import pygame

BG_PATH = 'resources/ui/bg.png'
BTN_PATH = 'resources/ui/button.png'
LOST_PATH = 'resources/ui/lost.png'


class LostUI:
    """
    Class for displaying the lost UI
    """

    def __init__(self, dims):
        bg = pygame.image.load(BG_PATH).convert_alpha()
        self.bg = pygame.transform.scale(bg, (bg.get_width() * 4, bg.get_height() * 4))
        self.bg_loc = (dims[0] // 2 - self.bg.get_width() // 2, dims[1] // 2 - self.bg.get_height() // 2)

        self.text = pygame.image.load(LOST_PATH).convert_alpha()
        self.text_loc = (dims[0] // 2 - self.text.get_width() // 2, dims[1] // 2.5 - self.text.get_height() // 2)

        self.btn = pygame.image.load(BTN_PATH).convert_alpha()
        self.btn_loc = (dims[0] // 2 - self.btn.get_width() // 2, dims[1] // 3 * 2 - self.btn.get_height() // 2)
        self.btn_rect = self.btn.get_rect().move(self.btn_loc)

    def on_click(self):
        """
        Handle 'play again' button click
        :return:
        """
        # Check if clicked on btn
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.btn_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            return True

    def draw(self, screen):
        """
        Draw the lost UI
        :param screen: screen instance
        :return:
        """
        screen.blit(self.bg, self.bg_loc)
        screen.blit(self.text, self.text_loc)
        screen.blit(self.btn, self.btn_loc)
