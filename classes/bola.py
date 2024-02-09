import pygame
# Classe para representar a bola
class Bola(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        
        # Carrega a imagem da bola e redefine o tamanho
        self.image = pygame.image.load('imagens/bola_de_canhao.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))

        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.y -= 2  # Movimento da bola para cima