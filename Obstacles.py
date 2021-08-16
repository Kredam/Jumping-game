from pygame import *
import pygame

# (566, 701)

class Obstacles:
    def __init__(self, x, y, width, height, velocity, image=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.counter = 0
        self.image = image
        self.spawned = False

    def move(self):
        self.x -= self.velocity

    def load_image(self, path):
        self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
