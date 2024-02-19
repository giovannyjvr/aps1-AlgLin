import pygame
from .tamanhos import *
import numpy as np

class Passaro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('imagens/passaro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70,100))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 550))

        self.initial_position = np.array([SCREEN_WIDTH/5,SCREEN_HEIGHT - 50])
        self.initial_speed = np.array([16, -10])
    def draw(self):
        screen.blit(self.image, self.rect)