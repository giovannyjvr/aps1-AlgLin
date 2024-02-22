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

def carregar_audio(caminho):
    try:
        pygame.mixer.init()
        som = pygame.mixer.Sound(caminho)
        return som
    except pygame.error as mensagem_erro:
        print("Erro ao carregar o som:", mensagem_erro)
        return None
    
def last_update(self):
        ultimo_tempo = state["last_updated"]
        tempo = pygame.time.get_ticks()
        delta_t = (tempo-ultimo_tempo)/1000
        state["last_updated"] = tempo
        self.sprites.update(delta_t)

def reproduzir_audio(audio, duracao=650):
    try:
        pygame.mixer.init()
        audio.play(maxtime=duracao)  # Define a duração máxima do som em milissegundos
    except Exception as e:
        print("Erro ao reproduzir o áudio:", e)

def reproduzir_fundo(audio, loop=True):
    try:
        pygame.mixer.init()
        if loop:
            audio.play(-1)  # Reproduz em loop infinito
        else:
            audio.play()  # Reproduz uma vez
    except Exception as e:
        print("Erro ao reproduzir o áudio:", e)

