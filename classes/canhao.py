import pygame
from .cores import Cores
from .tamanhos import *

# Classe para representar o canhão
class Canhao(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('imagens/canhao.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,150))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))

    def draw(self):
        screen.blit(self.image, self.rect)