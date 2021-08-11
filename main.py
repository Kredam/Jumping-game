from Obstacles import *
import pygame
from Menu import *
import Character
import glob

# player
player_size = (150, 150)
player_coordinates = [0, 575]
player = Character.Character(player_coordinates[0], player_coordinates[1], player_size[0], player_size[1])
player_img_standing = pygame.image.load(
    "/home/kadam/Projects/Python/TheEpicSwordGuy/assets/character/standing/tile000.png")
running = [pygame.transform.scale(pygame.image.load(img), [player.width, player.height]) for img in glob.glob(
    "/home/kadam/Projects/Python/TheEpicSwordGuy/assets/character/moving/*.png")]
walk_left = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load(img), [player.width, player.height]), True, False)
    for img in
    glob.glob("/home/kadam/Projects/Python/TheEpicSwordGuy/assets/character/moving/*.png")]
death = [pygame.transform.scale(pygame.image.load(img), [player.width, player.height]) for img in
         glob.glob("/home/kadam/Projects/Python/TheEpicSwordGuy/assets/character/death/*.png")]

# window
window_size = width, height = 1280, 768
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("The Epic Sword Guy")
bg = pygame.transform.scale(pygame.image.load(
    "/home/kadam/Projects/Python/TheEpicSwordGuy/assets/background/Background.png"), window_size)
game_over = pygame.transform.scale(
    (pygame.image.load("/home/kadam/Projects/Python/TheEpicSwordGuy/assets/Menu/GameOver.png")),
    [880, 668])

# menu
menu = Menu(24)

# obstacles
lava = Obstacles(window_size[0], 490, 300, 285, 20)
lava.load_image("/home/kadam/Projects/Python/TheEpicSwordGuy/assets/Obstacles/lava/lava0.png")

spikes = Obstacles(window_size[0], 570, 300, 285, 0)
spikes.load_image("/home/kadam/Projects/Python/TheEpicSwordGuy/assets/Obstacles/spikes.png")

list_of_obstacles = [lava, spikes]
item = 0
FPS = 27


def redraw_window():
    window.blit(bg, (0, 0))
    if menu.game_started:
        key = pygame.key.get_pressed()
        player.movement(key)
        spawn_obstacle()
        player_animation()
        menu.draw_score(window, window_size[0] - 200, 50, player.score)
    else:
        menu.draw_main_menu(window, window_size[0], window_size[1])

    pygame.display.update()


def spawn_obstacle():
    window.blit(list_of_obstacles[0].image, (list_of_obstacles[0].x, list_of_obstacles[0].y))
    window.blit(list_of_obstacles[1].image, (list_of_obstacles[1].x, list_of_obstacles[1].y))
    if player.alive:
        list_of_obstacles[0].move()
        list_of_obstacles[1].move()
    if list_of_obstacles[0].x + list_of_obstacles[0].width < 0:
        list_of_obstacles[0].x = window_size[0]
    if list_of_obstacles[1].x + list_of_obstacles[1].width < 0:
        list_of_obstacles[1].x = window_size[0]
    if list_of_obstacles[0].x < 500:
        list_of_obstacles[1].velocity = 20


def player_animation():
    if player.moving_left or player.moving_right:
        player.running_animation = 0
        if player.movement_animation_counter >= FPS:
            player.movement_animation_counter = 0
        if player.moving_right:
            window.blit(running[player.movement_animation_counter // 4], (player.x, player.y))
            player.movement_animation_counter += 1
        if player.moving_left:
            window.blit(walk_left[player.movement_animation_counter // 4], (player.x, player.y))
            player.movement_animation_counter += 1
    elif player.alive:
        player.movement_animation_counter = 0
        if player.running_animation >= FPS:
            player.running_animation = 0
        window.blit(running[player.running_animation // 4], (player.x, player.y))
        player.running_animation += 1

    lava_damage = player.damage_player(list_of_obstacles, 0)
    spike_damage = player.damage_player(list_of_obstacles, 1)
    while player.lives > 0:
        try:
            print(next(lava_damage))
            print(next(spike_damage))
        except StopIteration:
            break

    if player.alive is False and player.death_counter != FPS:
        window.blit(death[player.death_counter // 8], (player.x, player.y))
        player.death_counter += 1
    if player.death_counter == FPS:
        window.blit(death[-1], (player.x, player.y))
    if not player.alive:
        window.blit(game_over, (200, 100))


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window()


main()
