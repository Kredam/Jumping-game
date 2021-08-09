import pygame as pg
import pygame.freetype

colors = {
    "grey_light": pg.Color(200, 200, 200),
    "grey_dark": pg.Color(100, 100, 100),
    "green": pg.Color(50, 255, 63),
    "red": pg.Color(220, 30, 30),
    "blue": pg.Color(50, 75, 245),
}


class menu:
    def __init__(self, font_size, font_type=pygame.freetype.get_default_font()):
        pygame.freetype.init()
        self.font_type = font_type
        self.font_size = font_size

    def draw_score(self, surface, x_position, y_position, score=""):
        font = pygame.freetype.SysFont(self.font_type, self.font_size)
        font.render_to(surface, (x_position, y_position), "Score = " + str(score), colors["grey_dark"], self.font_size)
