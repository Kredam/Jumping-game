from Obstacles import *
from pygame import *
import random
import pygame
import Character
import glob

#player
player_size=(150, 150)
player_coordinates=[0, 575]
player = Character.Character(player_coordinates[0], player_coordinates[1], player_size[0], player_size[1])
player_img_standing = pygame.image.load("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/character/standing/tile000.png")
player_img_standing=pygame.transform.scale((player_img_standing), [player.width, player.height])
walk_right=[ pygame.transform.scale(pygame.image.load(img), [player.width,player.height]) for img in glob.glob("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/character/moving/*.png")]
walk_left=[ pygame.transform.flip(pygame.transform.scale(pygame.image.load(img), [player.width,player.height]), True, False) for img in glob.glob("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/character/moving/*.png")]
standing=[pygame.transform.scale(pygame.image.load(img), [player.width, player.height]) for img in glob.glob("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/character/standing/*.png")]
death=[pygame.transform.scale(pygame.image.load(img), [player.width, player.height]) for img in glob.glob("/home/adam/Downloads/ezgif-6-dcdffdad9d70-png-42x42-sprite-png/*.png") ]

#window
window_size = width, height = 1280, 768
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("The Epic Sword Guy")
bg = pygame.transform.scale(pygame.image.load("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/background/Background.png"), window_size)
game_over=pygame.transform.scale((pygame.image.load("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/Menu/GameOver.png")), [880, 668])

#load all moving png files to a list with list comprehession

#obstacles
lava = Obstacles(window_size[0], 490, 300, 285, 10)
lava.load_image("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/Obstacles/lava/lava0.png")

lava2 = Obstacles(window_size[0], 490, 300, 285, 10)
lava.load_image("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/Obstacles/lava/lava0.png")

spikes = Obstacles(window_size[0], 570, 300, 285, 10)
spikes.load_image("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/Obstacles/spikes.png")

spikes2 = Obstacles(window_size[0], 490, 300, 285, 10)
spikes2.load_image("/home/adam/Projects/Python/Practice_And_Learning/TheEpicSwordGuy/assets/Obstacles/spikes.png")

list_of_obstacles=[lava, spikes, lava2, spikes2]
print(type(list_of_obstacles))
item=0
FPS=27

def redraw_window():
    window.blit(bg, (0,0))

    spawn_obstacle()
    
    player_animation()
    if lava.counter>=FPS or player.death_counter>FPS:
        lava.counter=0
        player.death_counter=0
    else:
        lava.counter+=1

    pygame.display.update()

def spawn_obstacle():
    global item
    print(item)
    obstacle_spawned=list_of_obstacles[item]
    if obstacle_spawned.spawned==False:
        window.blit(obstacle_spawned.image, (obstacle_spawned.x, obstacle_spawned.y))
        obstacle_spawned.counter+=1
        if player.alive:
            obstacle_spawned.move()
        obstacle_spawned.spawned==True
        if item == 0 and list_of_obstacles[1].x < 0:
            list_of_obstacles[1].x == window_size[0]
        if item == 1 and list_of_obstacles[0].x < 0:
            list_of_obstacles[0].x == window_size[0]
        if(obstacle_spawned.x + obstacle_spawned.width <0):
            if(item == 1):
                item = 0
            item+=1

def player_animation():
    if player.moving_left or player.moving_right:
        player.standing_animation_counter=0
        if player.movement_animation_counter >= FPS:
            player.movement_animation_counter = 0
        if player.moving_left:
            window.blit(walk_left[player.movement_animation_counter//4], (player.x, player.y))
            player.movement_animation_counter+=1
        if player.moving_right:
            window.blit(walk_right[player.movement_animation_counter//4], (player.x, player.y))
            player.movement_animation_counter+=1
    elif player.alive:
        player.movement_animation_counter=0
        if player.standing_animation_counter >= FPS:
            player.standing_animation_counter=0
        window.blit(standing[player.standing_animation_counter//8], (player.x, player.y))
        player.standing_animation_counter+=1
    
    #player.death(list_of_obstacles, item)
    if player.alive == False and player.death_number!=FPS:
        window.blit(death[player.death_counter//6], (player.x, player.y))
        player.death_counter+=1
        player.death_number+=1
    if player.death_number == FPS:
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

        key = pygame.key.get_pressed()
        player.movement(key)

        redraw_window()

main()