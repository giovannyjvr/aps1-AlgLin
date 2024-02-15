import pygame
# Classe para representar a bola
class Bola(pygame.sprite.Sprite):
    def __init__(self):
        
        super().__init__()
        WHITE = (255, 255, 255)
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    # def update(self):
    #     pass  # Adicione aqui a lógica de atualização da bola

    #     self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.y -= 2  # Movimento da bola para cima