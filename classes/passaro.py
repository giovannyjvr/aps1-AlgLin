import pygame
from .tamanhos import *

class Passaro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('imagens/passaro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70,100))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 550))

    def draw(self):
        screen.blit(self.image, self.rect)