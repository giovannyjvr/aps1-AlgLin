import pygame
from assets import *
from state import *

def imprime(self,texto,fonte,cor,x,y):
    texto = fonte.render(f"{texto}", True, cor)
    self.window.blit(texto, (x, y))

def contorno(self,texto,fonte,cor,x,y,cor_contorno):
    imprime(self,texto, fonte, cor_contorno,(x-1),(y+1))
    imprime(self,texto, fonte, cor_contorno,(x-1),(y-1))
    imprime(self,texto, fonte, cor_contorno,(x+1),(y+1))
    imprime(self,texto, fonte, cor_contorno,(x+1),(y-1))
    imprime(self,texto, fonte, cor,(x),(y))


def fps(self):
    fonte = assets["fonte"]
    fonte = pygame.font.Font(fonte,12)
    fps = 0
    t0 = state["t0"]
    t1 = pygame.time.get_ticks()
    if t0 > 0:
        fps = 1000/(t1 - t0)
    state["t0"] = t1
    texto_fps = fonte.render(f'fps: {fps:.2f}', True, (255,255,255))
    return texto_fps
