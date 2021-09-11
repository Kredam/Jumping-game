import pygame

class CustomEvents:
    def __init__(self):
        pygame.init()
        self.INCREASE_SPEED = pygame.USEREVENT
        pygame.time.set_timer(self.INCREASE_SPEED, 24000)
        self.DELAY_SPAWN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.DELAY_SPAWN, 2500)
