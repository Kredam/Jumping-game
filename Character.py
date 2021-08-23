import glob
import time
import os
import timeit

from pygame import *
import pygame

health_scale = (300, 300)
health_image = [pygame.transform.scale(pygame.image.load(img), [health_scale[0], health_scale[1]]) for img in
                glob.glob(os.path.join("assets/character/Health", "*.png"))]
health = {
    "1": health_image[0],
    "2": health_image[2],
    "3": health_image[1],
    "0": health_image[3]
}


class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.nr_of_times_damaged = 0
        self.timer = 0
        self.width = width
        self.height = height
        self.lives = 3
        self.damaged = False
        self.alive = True
        self.moving_left = False
        self.moving_right = False
        self.wound = False
        self.isJump = False
        self.movement_speed = 10
        self.movement_animation_counter = 0
        self.running_animation = 0
        self.death_counter = 0
        self.jumpCount = 10
        self.score = 0
        self.name = ""
        self.load_images()

    def draw_remaining_health(self, surface):
        if self.lives == 3:
            surface.blit(health["2"], (950, -5))
        elif self.lives == 2:
            surface.blit(health["3"], (950, -5))
        elif self.lives == 1:
            surface.blit(health["1"], (950, -5))
        else:
            surface.blit(health["0"], (950, -5))

    # fix collision detection
    def check_collision(self, obstacles, item):
        if obstacles[item].x + obstacles[item].width > self.x > obstacles[item].x - 35 and self.y + self.height >= obstacles[item].y:
            return True
        else:
            return False

    def set_username(self, name):
        if len(self.name) == 0:
            self.name = name
        else:
            self.name = ""
            self.name = name

    def damage_player(self, obstacle, item):
        if self.check_collision(obstacle, item) and self.damaged is False:
            self.lives -= 1
        if self.lives <= 0:
            self.alive = False

    def border_check(self, max_x):
        if self.x - self.movement_speed < 0:
            self.x = 0
        if self.x + self.movement_speed > max_x - self.width:
            self.x = max_x - self.width

    def movement(self, key):
        if key[pygame.K_LEFT] and self.alive:
            self.x -= self.movement_speed
            self.moving_left = True
            self.moving_right = False
        elif key[pygame.K_RIGHT] and self.alive:
            self.x += self.movement_speed
            self.score += self.movement_speed
            self.moving_right = True
            self.moving_left = False
        else:
            self.movement_animation_counter = 0
            self.moving_right = False
            self.moving_left = False
        if self.alive:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.jumpCount = 10

    def load_images(self):
        self.running = [pygame.transform.scale(pygame.image.load(img), [self.width, self.height]) for img in glob.glob(
            os.path.join("assets/character/moving", "*.png"))]
        self.walk_left = [
            pygame.transform.flip(pygame.transform.scale(pygame.image.load(img), [self.width, self.height]), True, False)
            for img in
            glob.glob(os.path.join("assets/character/moving", "*.png"))]
        self.death = [pygame.transform.scale(pygame.image.load(img), [self.width, self.height]) for img in
                      glob.glob(os.path.join("assets/character/Death", "*.png"))]

    def player_animation(self, surface, fps):
        if self.alive:
            if self.moving_left or self.moving_right:
                self.running_animation = 0
                if self.movement_animation_counter >= fps:
                    self.movement_animation_counter = 0
                if self.moving_right:
                    surface.blit(self.running[self.movement_animation_counter // 4], (self.x, self.y))
                    self.movement_animation_counter += 1
                if self.moving_left:
                    surface.blit(self.walk_left[self.movement_animation_counter // 4], (self.x, self.y))
                    self.movement_animation_counter += 1
            else:
                self.movement_animation_counter = 0
                if self.running_animation >= fps:
                    self.running_animation = 0
                surface.blit(self.running[self.running_animation // 4], (self.x, self.y))
                self.running_animation += 1
        else:
            if self.death_counter != fps:
                surface.blit(self.death[self.death_counter // 8], (self.x, self.y))
                self.death_counter += 1
            if self.death_counter == fps:
                surface.blit(self.death[-1], (self.x, self.y))

