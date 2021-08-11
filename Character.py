from pygame import *
import pygame


class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lives = 3
        self.alive = True
        self.moving_left = False
        self.moving_right = False
        self.wound = False
        self.isJump = False
        self.movement_speed = 5
        self.movement_animation_counter = 0
        self.running_animation = 0
        self.death_counter = 0
        self.jumpCount = 10
        self.score = 0

    def wounded(self, obstacles, item):
        if obstacles[item].x + obstacles[item].width > self.x > obstacles[item].x and self.y >= obstacles[item].y:
            return True

    def damage_player(self, obstacle, item):
        if self.wounded(obstacle, item) and self.alive:
            remaining = self.lives
            self.lives -= 1
            print(self.lives)
            yield remaining

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

