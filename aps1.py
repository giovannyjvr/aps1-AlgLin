# Pacotes necessários. Resolva essas dependências antes de prosseguir!
import matplotlib.pyplot as plt
import numpy as np
import pygame
from pygame.locals import *


pygame.init()

# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
FPS = 60  # Frames per Second

BLACK = (0, 0, 0)
COR_PERSONAGEM = (30, 200, 20)

# Inicializar posicoes
s0 = np.array([50,200])
# v0 = np.array([10, -10])
# a = np.array([0, 0.2])
#Modificado
v0 = np.array([15, -15])
a = np.array([0, 0.5])
v = v0
s = s0
clicou = False
# Personagem
personagem = pygame.Surface((5, 5))  # Tamanho do personagem
personagem.fill(COR_PERSONAGEM)  # Cor do personagem

rodando = True
while rodando:
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
    mouse_presses = pygame.mouse.get_pressed()
    if mouse_presses[0]:
        pos = pygame.mouse.get_pos()
        if pos[0] > 600 and pos[0] < 640 and pos[1]>600 and pos[1]<640:
            clicou = True
    
    if s[0]<10 or s[0]>780 or s[1]<10 or s[1]>780: # Se eu chegar ao limite da tela, reinicio a posição do personagem
        y = pygame.mouse.get_pos()
        mod = np.linalg.norm(y-s0)
        x = 1/mod
        
        if clicou:
            y = (y-s0)*x*20
        else:
            y = (y-s0)*x*5
        s, v = s0, y 

    # Controlar frame rate
    clock.tick(FPS)

    # Processar posicoes
    

    v = v + a
    s = s + 0.1 * v

    # Desenhar fundo
    screen.fill(BLACK)

    # Desenhar personagem
    rect = pygame.Rect(s, (10, 10))  # First tuple is position, second is size.
    screen.blit(personagem, rect)

    if clicou:
        pygame.draw.polygon(screen, (255,0,0), [(600, 600), (640, 600), (640, 640), (600, 640)])
    else: 
        pygame.draw.polygon(screen, (0,255,0), [(600, 600), (640, 600), (640, 640), (600, 640)])

    # Update!
    pygame.display.update()

# Terminar tela
pygame.quit()