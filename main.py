
from random import randint
import pygame
import numpy as np
import math
from assets import *
from state import *
from funcoes import *



def last_update(self):
        ultimo_tempo = state["last_updated"]
        tempo = pygame.time.get_ticks()
        delta_t = (tempo-ultimo_tempo)/1000
        state["last_updated"] = tempo
        self.sprites.update(delta_t)

class Jogo:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.alvo = pygame.sprite.Group()
        self.planeta = pygame.sprite.Group()

        self.window = Jogo.inicializa(self)
        self.jogador = Jogador(self.alvo)

        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()

        coord_alvo = assets["coord_alvo_1"]
        for i in range(len(coord_alvo)):
            Alvo(self.sprites, self.alvo, coord_alvo[i][0], coord_alvo[i][1])

        coord_planeta = assets["coord_planetas_1"]
        for i in range(len(coord_planeta)):
            Planeta(self.sprites, self.planeta, coord_planeta[i][0], coord_planeta[i][1])
        
        self.sprites.add(self.jogador)

        
        self.fonte = pygame.font.Font(assets["fonte_padrao"], 12)

        self.tela = "tela_inicial"

        self.flag_tiro = False
        self.vel = state["vel"]
        self.window = assets["window"]
        self.game_loop()
            
    
    def recebe_eventos(self):
        velocidade = 400
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.tela = "tela_over"
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.jogador.vel_y-=velocidade
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.jogador.vel_y+=velocidade
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.jogador.vel_y+=velocidade
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.jogador.vel_y-=velocidade
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Tiro(self.sprites, self.alvo, self.jogador, self.jogador.rect.x + 100, self.jogador.rect.y + 40, self.vel, self.planeta)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.0:
                    self.vel += 0.1             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >0.4 :
                    self.vel -= 0.1
        last_update(self)
        return "tela_jogo"

    

    def inicializa(self):
        pygame.init()
        self.window = assets["window"]
        pygame.display.set_caption("Jogo do Edu")
        
        
        # musica = pygame.mixer.Sound("assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg")
        if not(assets["musica_tocando"]):
            # musica.play()
            assets["musica_tocando"] = True
        return self.window
    
    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(assets["fundo"], (0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))

        fonte = pygame.font.Font(assets["fonte_padrao"],12)
       
        pos = pygame.mouse.get_pos()
        if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:  
            pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 120,self.jogador.rect.y +60), (pos[0], pos[1]))
        
        self.sprites.draw(self.window)
        pygame.display.update()
    
    def game_loop(self):
        telas = {
            "tela_inicial": TelaInicial(self.window, self.tela),
            "tela_jogo": self,
            "tela_jogo2": TelaJogo2(self.window, self.tela),
            "tela_over": TelaGameOver(self.window, self.tela)
        }

        tela_atual = telas[self.tela]
        while True:
            self.tela = tela_atual.recebe_eventos()
            if self.tela == False:
                break
            if state["flag_tela2"]:
                self.tela = "tela_jogo2"
            tela_atual = telas[self.tela]
            tela_atual.desenha()

class TelaJogo2:
    def __init__(self, window, tela):      
        self.sprites = pygame.sprite.Group()
        self.alvo = pygame.sprite.Group()
        self.planeta = pygame.sprite.Group()

       
        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()

        self.jogador = Jogador(self.alvo)
        self.sprites.add(self.jogador)

        coord_alvo = assets["coord_alvo_2"]
        Alvo(self.sprites, self.alvo, coord_alvo[0][0], coord_alvo[0][1])

        coord_planeta = assets["coord_planetas_2"]
        for i in range(len(coord_planeta)):
            Planeta(self.sprites, self.planeta, coord_planeta[i][0], coord_planeta[i][1])

        
        
        self.fonte = pygame.font.Font(assets["fonte_padrao"], 12)
        self.tela = tela
        
        self.flag_tiro = False
        state["vel"] = 1
        self.vel = state["vel"]
        self.window = window 

    def recebe_eventos(self):
        velocidade = 400

        for event in pygame.event.get():
            if event.type == pygame.QUIT or state["flag_tela2"] == False:
                return "tela_over"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.jogador.vel_y-=velocidade
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.jogador.vel_y+=velocidade
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.jogador.vel_y+=velocidade
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.jogador.vel_y-=velocidade
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Tiro(self.sprites, self.alvo, self.jogador, self.jogador.rect.x + 50, self.jogador.rect.y + 25, self.vel, self.planeta)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.5:
                    self.vel += 0.3             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >1.3 :
                    self.vel -= 0.3

        last_update(self)
        return "tela_jogo2"

    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(assets["fundo2"], (0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))

        pos = pygame.mouse.get_pos()
        if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:  
            pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 120,self.jogador.rect.y +60), (pos[0], pos[1]))
        
        self.sprites.draw(self.window)
        pygame.display.update()
       
class Jogador(pygame.sprite.Sprite):
    def __init__(self, planetas):
        pygame.sprite.Sprite.__init__(self)
        self.planetas = planetas
        image = assets["img_nave"]
        self.image_original = pygame.transform.rotate(image, 323)  # Rotação original da imagem
        self.image = self.image_original.copy()  # Cópia da imagem original para a transformação
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width / 5
        self.rect.y = 480 - self.rect.height

        self.vel_x = 0
        self.vel_y = 0
        

    def update(self, delta_t):

        self.rect.y = (self.rect.y + self.vel_y*delta_t)
        if self.rect.y + self.rect.height >= 600:
            self.rect.y = 600 - self.rect.height
        if self.rect.y < 0:
            self.rect.y = 0


class Planeta(pygame.sprite.Sprite):
    def __init__(self, sprites, planeta,  x, y):
        pygame.sprite.Sprite.__init__(self)
        image1 = assets["img_planeta1"]
        image2 = assets["img_planeta2"]
        imagens = [image1, image2]
        self.image = imagens[randint(0,1)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
        planeta.add(self)

class Tiro(pygame.sprite.Sprite):
    def __init__(self, sprites, alvo, jogador, x, y, vel, planeta):
        super().__init__()
        self.velo = vel
        self.planetas = planeta
        self.alvo = alvo

        self.original_image = assets["img_tiro"]
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.initial_v = state["initial_vel"]
        self.flag_tiro = True
        
        sprites.add(self)
        self.sprites = sprites

    def update(self, delta_t):
        if self.flag_tiro:
            posicao_mouse = pygame.mouse.get_pos()
            posicao_atual = np.array([self.rect.x, self.rect.y])
            mod = np.linalg.norm(posicao_mouse - posicao_atual)
            x = 1 / mod
            nova_v = (posicao_mouse - posicao_atual) * x * 2.5
            self.initial_v = nova_v
            self.flag_tiro = False

        forca = np.array([0,0])
        soma_no_x = 0
        soma_no_y = 0

        for planeta in self.planetas:
            x = planeta.rect.x
            y = planeta.rect.y
            
            tamanho_vetor_horizontal = x - self.rect.x
            tamanho_vetor_vertical = y - self.rect.y
            vetor = np.array([tamanho_vetor_horizontal, tamanho_vetor_vertical])
            vetor  = vetor / np.linalg.norm(vetor)
            forca = vetor*(5000/ (tamanho_vetor_horizontal**2 + tamanho_vetor_vertical**2)**0.5)
            soma_no_x += forca[0]
            soma_no_y += forca[1]
        

        self.rect.x += (self.initial_v[0] + soma_no_x/50) * self.velo
        self.rect.y += (self.initial_v[1] + soma_no_y/50) *  self.velo 

        
        C = 4000
        aceleracoes = []
        angulos = []
        
        for planeta in self.planetas:
            distancia = np.sqrt((self.rect.x - planeta.rect.x)**2 + (self.rect.y - planeta.rect.y)**2)
            aceleracao = C / distancia**2
            aceleracoes.append(aceleracao)
            angulo = np.arctan2(planeta.rect.y - self.rect.y, planeta.rect.x - self.rect.x)
            angulos.append(angulo)
            centro_planeta = planeta.rect.x +64, planeta.rect.y+64
            if abs(planeta.rect.x - self.rect.x) < 20 and abs(self.rect.y - planeta.rect.y) < 20:
                print(abs(planeta.rect.x  - self.rect.x), abs(self.rect.y - planeta.rect.y))
                self.kill()
        ax = 0
        ay = 0
        for i in range(len(aceleracoes)):
            ax += aceleracoes[i]*np.cos(angulos[i])/4
            ay += aceleracoes[i]*np.sin(angulos[i])/4

        if ax > 1:
            ax = 1
        if ax < -1:
            ax = -1
        if ay > 1:
            ay = 1
        if ay < -1:
            ay = -1
        
        self.initial_v += np.array([ax, ay])
        self.rect.x += self.initial_v[0] * self.velo
        self.rect.y += self.initial_v[1] * self.velo

        lista = pygame.sprite.spritecollide(self, self.alvo, True)
        for alvo in lista:
            self.sprites.remove(self)
            state["flag_tela2"] = True

        if self.rect.x > 790 or self.rect.x < 0 or self.rect.y > 600 or self.rect.y < 0:
            self.kill()

class Alvo(pygame.sprite.Sprite):
    def __init__(self, sprites, alvo, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets["img_alvo"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
        alvo.add(self)

class Estrela:
    def __init__(self, quant_estrelas):
        self.quant_estrelas = quant_estrelas
    def gera_estrelas(self):
        estrelas = []
        for i in range(self.quant_estrelas):
            lista = []
            lista.append(randint(0,800))
            lista.append(randint(0,600))
            lista.append(randint(1,3))
            estrelas.append(lista)
        return estrelas
    

class TelaInicial:
    def __init__(self, window, tela):
        pygame.init()
        self.window = window
        self.tela = tela
        

    def recebe_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                return "tela_jogo"
        return "tela_inicial"
    
    def desenha(self):
        fonte = assets["fonte_padrao"]
        fonte_titulo = pygame.font.Font(fonte, 34)
        fonte_24 = pygame.font.Font(fonte, 24)
        fonte_26 = pygame.font.Font(fonte, 42)
        fonte = pygame.font.Font(fonte, 40)

        fundo = assets["fundo_inicial"]
        self.window.blit(fundo, (0,0))
        
        contorno(self, "Ovni Wars", fonte_titulo, (0,0,0),300,50, (255,255,255))

        contorno(self, "Aperte 'Espaço'", fonte, (255,0,0),265,201,(0,0,0))
        contorno(self, "para iniciar", fonte, (255,0,0),270,241,(0,0,0))
        contorno(self, "Instruções:", fonte_titulo, (255,255,0),5,360,(0,0,0))
        contorno(self, "(Q) para diminuir a", fonte_24, (0,0,0),5,400,(255,255,255))
        contorno(self, "velocidade do tiro", fonte_24, (0,0,0),5,425,(255,255,255))
        contorno(self,"(E) para aumentar a",fonte_24,(0,0,0), 5,460,(255,255,255))
        contorno(self,"velocidade do tiro",fonte_24,(0,0,0), 5,485,(255,255,255))
        contorno(self,"(↑)(↓) para mexer",fonte_24,(0,0,0), 5,525,(255,255,255))
        contorno(self,"a nave",fonte_24,(0,0,0), 5,550,(255,255,255))

        pygame.display.update()

        
        
class TelaGameOver:
    def __init__(self, window, tela):
        pygame.init()
        self.window = window
        self.tela = tela

    def recebe_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            # if evento.type == pygame.KEYDOWN:
            #     return 
        return "tela_over"
    
    def desenha(self):
        fonte_geral = assets["fonte"]
        fonte = pygame.font.Font(fonte_geral, 44)
        fonte2 = pygame.font.Font(fonte_geral, 24)

        fundo = assets["fundo_final"]
        self.window.blit(fundo, (0,0))
        imprime(self,"Você perdeu",fonte,(255,255,255), 290, 50)
        textinho = "testandoooooo"
        imprime(self,textinho,fonte2,(0,0,255), 20, 40)
        self.texto = fonte2.render("Sua pontuação foi: ", True, (255,255,0))
        self.window.blit(self.texto, (100, 130))
        self.texto = fonte2.render("ZZZ", True, (255,0,0))
        self.window.blit(self.texto, (100, 160))
        pygame.display.update()

