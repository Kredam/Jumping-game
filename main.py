import os
import random
import time

from Obstacles import *
import pygame
from Menu import *
import Character
import glob

# player
player_size = (75, 150)
player_coordinates = [0, 575]
player_name = ""
player = Character.Character(player_coordinates[0], player_coordinates[1], player_size[0], player_size[1])

# window
window_size = width, height = 1280, 768
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("The Epic Sword Guy")
bg = pygame.transform.scale(pygame.image.load(
    os.path.join("assets/background", "Background.png")), window_size)

# menu
menu = Menu(24)
# obstacles
lava = Obstacles(window_size[0], 700, 300, 75, 15)
lava.load_image(os.path.join("assets/Obstacles/lava", "lava0.png"))

spikes = Obstacles(window_size[0], 700, 300, 285, 0)
spikes.load_image(os.path.join("assets/Obstacles", "spikes.png"))

list_of_obstacles = [lava, spikes]
item = 0
FPS = 27


def redraw_window():
    window.blit(bg, (0, 0))
    if menu.game_started:
        menu.back_to_main(window, player, list_of_obstacles)
        key = pygame.key.get_pressed()
        spawn_obstacle()
        player.border_check(window_size[0])
        player.movement(key)
        player.draw_remaining_health(window)
        player.player_animation(window, FPS)
        player.damage_player(list_of_obstacles, 0)
        player.damage_player(list_of_obstacles, 1)
        menu.draw_text(window, window_size[0] - 200, 50, f"Score = {player.score}")
        if player.alive is False:
            window.blit(menu.game_over_png, (300, 85))
            menu.draw_text(window, window_size[0]-400, window_size[1]-100, "Please insert your Username!")
    elif menu.leaderBoard_pressed:
        window.fill(0)
        menu.show_leaderboard(window, window_size[0], window_size[1])
        menu.back_to_main(window, player, list_of_obstacles)
        # menu.show_leaderboard(window, window_size[0], window_size[1])
    else:
        menu.draw_main_menu(window, window_size[0], window_size[1])

    pygame.display.update()


def spawn_obstacle():
    distance = random.choice([400, 600, 800])
    window.blit(list_of_obstacles[0].image, (list_of_obstacles[0].x, list_of_obstacles[0].y))
    window.blit(list_of_obstacles[1].image, (list_of_obstacles[1].x, list_of_obstacles[1].y))
    if player.alive:
        list_of_obstacles[0].move()
        list_of_obstacles[1].move()
    if list_of_obstacles[0].x + list_of_obstacles[0].width < 0:
        list_of_obstacles[0].x = window_size[0]
    if list_of_obstacles[1].x + list_of_obstacles[1].width < 0:
        list_of_obstacles[1].x = window_size[0]
    if list_of_obstacles[0].x < distance:
        list_of_obstacles[1].velocity = 15

#kuki
def main():
    run = True
    clock = pygame.time.Clock()
    global player_name

    while run:
        clock.tick(FPS)
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False
            if evt.type == KEYDOWN and menu.game_started and player.alive is False:
                if evt.unicode.isalpha():
                    player_name += evt.unicode
                if evt.key == K_BACKSPACE:
                    player_name = player_name[:-1]
                if evt.key == K_RETURN:
                    player.set_username(player_name)
                    player_name = ""
                    menu.save_player_stats(player)
                    menu.restart_game(player, list_of_obstacles)
        menu.draw_text(window, window_size[0]-len(player_name)*15, window_size[1], player_name)
        pygame.display.update()
        redraw_window()

main()
