import os
import csv
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
back_button = pygame.transform.scale(pygame.image.load(os.path.join("assets/Menu", "Back.png")), (100, 100))


class Menu:
    def __init__(self, font_size, font_type=pygame.freetype.get_default_font()):
        pygame.freetype.init()
        self.leaderboard_players = {}
        self.game_over_png = pygame.image.load(os.path.join("assets/Menu", "GameOver.png"))
        self.font_type = font_type
        self.font_size = font_size
        self.main_non_selected = True
        self.leaderBoard_pressed = False
        self.main_start_selected = False
        self.main_leaderboard_selected = False
        self.game_started = False

    def draw_text(self, surface, x_pos, y_pos, text):
        font2 = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 30)
        font2.render_to(surface, (x_pos/2, y_pos/2), text, (255, 0, 0))

    def menu_actions(self, mouse_x, mouse_y):
        if 811 >= mouse_x >= 475 and 291 >= mouse_y >= 205:
            if pygame.mouse.get_pressed(3) == (1, 0, 0):
                self.game_started = True
            self.main_start_selected = True
            self.main_non_selected = False
            self.main_leaderboard_selected = False
        elif 811 >= mouse_x >= 476 and 400 >= mouse_y >= 309:
            if pygame.mouse.get_pressed(3) == (1, 0, 0):
                self.load_player_stats()
                self.leaderBoard_pressed = True
            self.main_start_selected = False
            self.main_non_selected = False
            self.main_leaderboard_selected = True
        else:
            self.main_start_selected = False
            self.main_non_selected = True
            self.main_leaderboard_selected = False

    def restart_game(self, player, obstacles):
        #you have to make a sequence of list
        player.score = 0
        player.lives = 3
        player.x = 0
        player.alive = True
        obstacles[-1].velocity = 0
        for obstacle in obstacles:
            obstacle.x = 1280
        self.main_non_selected = True
        self.leaderBoard_pressed = False
        self.main_start_selected = False
        self.main_leaderboard_selected = False
        self.game_started = False

    def load_player_stats(self):
        with open('Result.csv', mode='r') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                if row["player_name"] != "player_name":
                    test = self.leaderboard_players[row["player_name"]] = int(row["player_score"])

    def save_player_stats(self, player):
        Header = ["player_name", "player_score"]
        with open('Result.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Header)
            writer.writeheader()
            writer.writerow({'player_name': player.name, 'player_score': player.score})

    def back_to_main(self, surface, player, obstacles):
        surface.blit(back_button, (10, 10))
        if 10 <= pygame.mouse.get_pos()[0] <= 110 and 10 <= pygame.mouse.get_pos()[1] <= 110 and pygame.mouse.get_pressed(3) == (1, 0, 0):
            self.restart_game(player, obstacles)

    def show_leaderboard(self, surface, surface_x, surface_y):
        sorted_leaderboard = sorted(self.leaderboard_players.items(), key=lambda kv: kv[1], reverse=True)
        leaderboard = sorted_leaderboard.__iter__()
        i = 1
        while i <= 5:
            try:
                surface_y += 100
                self.draw_text(surface, surface_x-400, surface_y-300, f"{i}., {str(leaderboard.__next__())}")
            except StopIteration:
                break
            i += 1

    def draw_main_menu(self, surface, surface_width, surface_height):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        self.menu_actions(mouse_x, mouse_y)
        if self.main_non_selected:
            surface.blit(non_selected_image, ((surface_width - menu_size[0]) / 2, (surface_height - menu_size[1]) / 2))
        if self.main_start_selected:
            surface.blit(start_selected_image,
                         ((surface_width - menu_size[0]) / 2, (surface_height - menu_size[1]) / 2))
        if self.main_leaderboard_selected:
            surface.blit(leaderboard_selected_image,
                         ((surface_width - menu_size[0]) / 2, (surface_height - menu_size[1]) / 2))
