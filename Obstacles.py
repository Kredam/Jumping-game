import pygame

# (566, 701)

class Obstacles:
    def __init__(self, x, y, width, height, velocity, image=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.times = True
        self.velocity = velocity
        self.counter = 0
        self.image = image
        self.spawned = False

    def increase_speed(self):
        if self.velocity < 55:
            self.velocity += 10

    def move(self):
        self.x -= self.velocity

    def set_velocity(self, velocity):
        if self.times:
            self.velocity = velocity
            self.times = False

    def load_image(self, path):
        self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
