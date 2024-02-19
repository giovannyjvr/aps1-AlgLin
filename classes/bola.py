import pygame
from .tamanhos import *
# Classe para representar a bola
class Bola(pygame.sprite.Sprite):
    def __init__(self, sprites):
        
        super().__init__()
        WHITE = (255, 255, 255)
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 60
        self.speed_y = -60

        sprites.add(self) 
        self.sprites = sprites 

    def update(self):
        self.rect.y -= 2  # Movimento da bola para cima