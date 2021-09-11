import pygame.event
from Obstacles import *
from Menu import *
import Character
from CustomEvents import *


# player
player_size = (75, 150)
player_coordinates = [0, 575]
player = Character.Character(player_coordinates[0], player_coordinates[1], player_size[0], player_size[1])

# window
window_size = width, height = 1280, 768
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("The Epic Sword Guy")
bg = pygame.transform.scale(pygame.image.load(
    os.path.join("assets/background", "Background.png")), window_size)

custom_events = CustomEvents()


# menu
menu = Menu(font_size=24)

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
        # speed going to be increased when the custom event id detected in the event queue
        if pygame.event.get(custom_events.INCREASE_SPEED) and list_of_obstacles[0].x + list_of_obstacles[0].width <= window_size[0] and list_of_obstacles[0].x >= 0 and list_of_obstacles[1].x + list_of_obstacles[1].width <= window_size[0] and list_of_obstacles[1].x > 0:
            list_of_obstacles[0].increase_speed()
            list_of_obstacles[1].increase_speed()
        menu.back_to_main(window, player, list_of_obstacles)
        menu.drag_game_over(player, menu, window, window_size)
        key = pygame.key.get_pressed()
        spawn_obstacle()
        player.border_check(window_size[0])
        player.movement(key)
        player.draw_remaining_health(window)
        player.player_animation(window, FPS)
        player.damage_player(list_of_obstacles, 0)
        player.damage_player(list_of_obstacles, 1)
        draw_text(window, window_size[0] - 200, 50, f"Score = {player.score}")
    elif menu.leaderBoard_pressed:
        window.fill(0)
        menu.show_leaderboard(window, window_size[0], window_size[1])
        menu.back_to_main(window, player, list_of_obstacles)
    else:
        menu.draw_main_menu(window, window_size[0], window_size[1])

    pygame.display.update()


def spawn_obstacle():
    window.blit(list_of_obstacles[0].image, (list_of_obstacles[0].x, list_of_obstacles[0].y))
    window.blit(list_of_obstacles[1].image, (list_of_obstacles[1].x, list_of_obstacles[1].y))
    if player.alive:
        list_of_obstacles[0].move()
        # the 2 object spawn is delayed to avoid object overlap
        if pygame.event.get(custom_events.DELAY_SPAWN) and list_of_obstacles[0].x + list_of_obstacles[0].width < list_of_obstacles[1].x:
            list_of_obstacles[1].set_velocity(15)
        list_of_obstacles[1].move()
    if list_of_obstacles[0].x + list_of_obstacles[0].width < 0:
        list_of_obstacles[0].x = window_size[0]
    if list_of_obstacles[1].x + list_of_obstacles[1].width < 0:
        list_of_obstacles[1].x = window_size[0]


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False
            if evt.type == pygame.KEYDOWN and menu.game_started and player.alive is False:
                if evt.unicode.isalpha():
                    player.name += evt.unicoded
                if evt.key == pygame.K_BACKSPACE:
                    player.name = player.name[:-1]
                if evt.key == pygame.K_RETURN:
                    menu.save_player_stats(player)
                    menu.restart_game(player, list_of_obstacles)
        draw_text(window, window_size[0]-len(player.name)*15, window_size[1], player.name)
        pygame.display.update()
        redraw_window()


main()
