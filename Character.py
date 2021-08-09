from pygame import *
import pygame


class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alive = True
        self.moving_left = False
        self.moving_right = False
        self.wounded = False
        self.isJump = False
        self.movement_speed = 20
        self.movement_animation_counter = 0
        self.running_animation = 0
        self.death_counter = 0
        self.jumpCount = 10
        self.score = 0

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

    def death(self, obstacles, item):
        if obstacles[item].x + obstacles[item].width > self.x > obstacles[item].x and self.y >= obstacles[item].y:
            self.alive = False
