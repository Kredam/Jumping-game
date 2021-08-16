import os

import pygame as pg
from pygame.locals import *
import pygame
import pygame.freetype

colors = {
    "grey_light": pg.Color(200, 200, 200),
    "grey_dark": pg.Color(100, 100, 100),
    "green": pg.Color(50, 255, 63),
    "red": pg.Color(220, 30, 30),
    "blue": pg.Color(50, 75, 245),
}

menu_size = (1000, 750)

non_selected_image = pygame.transform.scale(
    pygame.image.load(os.path.join("assets/Menu", "Main.png")), (menu_size[0], menu_size[1]))
start_selected_image = pygame.transform.scale(
    pygame.image.load(os.path.join("assets/Menu", "StartSelected.png")),
    (menu_size[0], menu_size[1]))
leaderboard_selected_image = pygame.transform.scale(
    pygame.image.load(os.path.join("assets/Menu", "LeaderboardSelected.png")),
    (menu_size[0], menu_size[1]))


class Menu:
    def __init__(self, font_size, font_type=pygame.freetype.get_default_font()):
        pygame.freetype.init()
        self.font_type = font_type
        self.font_size = font_size
        self.main_non_selected = True
        self.main_start_selected = False
        self.main_leaderboard_selected = False
        self.game_started = False

    def draw_score(self, surface, x_position, y_position, score=""):
        font = pygame.freetype.SysFont(self.font_type, self.font_size)
        font.render_to(surface, (x_position, y_position), "Score = " + str(score), colors["grey_dark"], self.font_size)

    def menu_actions(self, mouse_x, mouse_y):
        # hardcoded for now, will be changed at the end of the project
        if 811 >= mouse_x >= 475 and 291 >= mouse_y >= 205:
            if pygame.mouse.get_pressed(3) == (1, 0, 0):
                self.game_started = True
            self.main_start_selected = True
            self.main_non_selected = False
            self.main_leaderboard_selected = False
        elif 811 >= mouse_x >= 476 and 400 >= mouse_y >= 309:
            self.main_start_selected = False
            self.main_non_selected = False
            self.main_leaderboard_selected = True
        else:
            self.main_start_selected = False
            self.main_non_selected = True
            self.main_leaderboard_selected = False

    def check_game_ended(self, player_alive):
        if player_alive is False and self.game_started:
            self.game_started = False
            self.main_non_selected = True

    def leaderboard(self):
        return 0

    def draw_main_menu(self, surface, surface_width, surface_height):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        self.menu_actions(mouse_x, mouse_y)
        # left upper corner x = 476, y = 309
        # right lower corner x = 811, y = 400
        if self.main_non_selected:
            surface.blit(non_selected_image, ((surface_width - menu_size[0]) / 2, (surface_height - menu_size[1]) / 2))
        if self.main_start_selected:
            surface.blit(start_selected_image,
                         ((surface_width - menu_size[0]) / 2, (surface_height - menu_size[1]) / 2))
        if self.main_leaderboard_selected:
            surface.blit(leaderboard_selected_image,
                         ((surface_width - menu_size[0]) / 2, (surface_height - menu_size[1]) / 2))
