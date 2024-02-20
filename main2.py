
from random import randint
import pygame
import numpy as np
import math

def fps(self):
    fonte = self.assets["fonte"]
    fonte = pygame.font.Font(fonte,12)
    fps = 0
    t0 = self.state["t0"]
    t1 = pygame.time.get_ticks()
    if t0 > 0:
        fps = 1000/(t1 - t0)
    self.state["t0"] = t1
    texto_fps = fonte.render(f'fps: {fps:.2f}', True, (255,255,255))
    return texto_fps

class Jogo:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.planetas = pygame.sprite.Group()
        self.alvo = pygame.sprite.Group()
        self.assets, self.state, self.window = Jogo.inicializa(self)
        self.jogador = Jogador(self.planetas)
        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()
        coord_estrelas = [[600, 400]]
        for i in range(1):
            Planeta(self.sprites, self.planetas, coord_estrelas[i][0], coord_estrelas[i][1])
        self.sprites.add(self.jogador)

        fonte = pygame.font.get_default_font()
        self.fonte = pygame.font.Font(fonte, 12)

        self.tela = "tela_inicial"

        self.flag_tiro = False
        self.vel = 1.0
        self.window = pygame.display.set_mode((800,600)) 
        self.game_loop()
            
    
    def recebe_eventos(self):
        velocidade = 400
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.jogador.vidas == 0:
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
                Tiro(self.sprites, self.planetas, self.jogador, self.jogador.rect.x + 50, self.jogador.rect.y + 25, self.vel, self.state)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.0:
                    self.vel += 0.1             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >0.4 :
                    self.vel -= 0.1
                            
        
        ultimo_tempo = self.state["last_updated"]
        tempo = pygame.time.get_ticks()
        delta_t = (tempo-ultimo_tempo)/1000
        self.state["last_updated"] = tempo
        self.sprites.update(delta_t)
        return "tela_jogo"

    def inicializa(self):
        pygame.init()
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Jogo do Edu")
        fundo = pygame.image.load("imagens/fundo.png")
        fundo = pygame.transform.scale(fundo, (800,600))
        fundo2 = pygame.image.load("imagens/fundo2.png")
        fundo2 = pygame.transform.scale(fundo2, (800,600))
        self.state = {
            "t0": 0,
            "vel_nave": [0,0],
            "posicao_nave": [300,400],
            "last_updated": 0,
            "flag_tela2": False
        }
        self.assets = {
            "fundo": fundo,
            "fundo2": fundo2,
            "flag_estrela": True,
            "fonte": "font/PressStart2P.ttf",
            "musica_tocando": False,
            "tela": "tela_inicial"
        }
        # musica = pygame.mixer.Sound("assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg")
        if not(self.assets["musica_tocando"]):
            # musica.play()
            self.assets["musica_tocando"] = True

        return self.assets,self.state, self.window
    
    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(self.assets["fundo"], (0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))

        pos = pygame.mouse.get_pos()
        if pos[0] < 300 and pos[1] < self.jogador.rect.y + 100 and pos[1] > self.jogador.rect.y - 100:  
            pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 50,self.jogador.rect.y + 25), (pos[0], pos[1]))
        
        self.sprites.draw(self.window)
        pygame.display.update()
    
    def game_loop(self):
        telas = {
            "tela_inicial": TelaInicial(self.window, self.tela),
            "tela_jogo": self,
            "tela_jogo2": TelaJogo2(self.window, self.tela, self.assets, self.state),
            "tela_over": TelaGameOver(self.window, self.tela)
        }

        tela_atual = telas[self.tela]
        while True:
            self.tela = tela_atual.recebe_eventos()
            if self.tela == False:
                break
            if self.state["flag_tela2"]:
                self.tela = "tela_jogo2"
            tela_atual = telas[self.tela]
            tela_atual.desenha()



class TelaJogo2:
    def __init__(self, window, tela, assets, state):      
        self.sprites = pygame.sprite.Group()
        self.planetas = pygame.sprite.Group()
        self.assets = assets
        self.state = state
       
        coord_estrelas = [[500, 200], [480, 500], [700, 350]]
        for i in range(3):
            Planeta(self.sprites, self.planetas, coord_estrelas[i][0], coord_estrelas[i][1])
        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()
        self.jogador = Jogador(self.planetas)
        self.sprites.add(self.jogador)
        
        fonte = pygame.font.get_default_font()
        self.fonte = pygame.font.Font(fonte, 12)
        self.tela = tela
        self.flag_tiro = False
        self.vel = 1.0
        self.window = window 

    def recebe_eventos(self):
        velocidade = 400

        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.jogador.vidas == 0 or self.state["flag_tela2"] == False:
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
                Tiro(self.sprites, self.planetas, self.jogador, self.jogador.rect.x + 50, self.jogador.rect.y + 25, self.vel, self.state)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.0:
                    self.vel += 0.1             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >0.4 :
                    self.vel -= 0.1
        ultimo_tempo = self.state["last_updated"]
        tempo = pygame.time.get_ticks()
        delta_t = (tempo-ultimo_tempo)/1000
        self.state["last_updated"] = tempo
        self.sprites.update(delta_t)
        return "tela_jogo2"

    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(self.assets["fundo2"], (0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))

        pos = pygame.mouse.get_pos()
        if pos[0] < 300 and pos[1] < self.jogador.rect.y + 100 and pos[1] > self.jogador.rect.y - 100:  
            pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 50,self.jogador.rect.y + 25), (pos[0], pos[1]))
        
        self.sprites.draw(self.window)
        pygame.display.update()
       


class Jogador(pygame.sprite.Sprite):
    def __init__(self, planetas):
        pygame.sprite.Sprite.__init__(self)

        self.flag_borda = False
        img_nave = pygame.image.load('imagens/navepft.png')
        image = pygame.transform.scale(img_nave, (100, 100))
        self.image_original = pygame.transform.rotate(image, 323)  # Rotação original da imagem
        self.image = self.image_original.copy()  # Cópia da imagem original para a transformação
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width / 5
        self.rect.y = 480 - self.rect.height

        self.vel_x = 0
        self.vel_y = 0
        self.planetas = planetas
        self.vidas = 3

    def update(self, delta_t):
        # Obtenha a posição do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calcule o vetor da posição do jogador para a posição do mouse
        vetor_x = mouse_x - self.rect.x
        vetor_y = mouse_y - self.rect.y
        # Calcule o ângulo entre o vetor e o eixo x usando arctan2
        angulo_rad = np.arctan2(vetor_y, vetor_x)
        # Converta o ângulo de radianos para graus
        angulo_deg = np.degrees(angulo_rad)
        # Rotacione a imagem original do jogador
        self.image = pygame.transform.rotate(self.image_original, -angulo_deg)
        # Atualize a posição do jogador
        self.rect = self.image.get_rect(center=self.rect.center)



class Tiro(pygame.sprite.Sprite):
    
    def __init__(self, sprites, planetas, jogador, x, y, vel, state):
        super().__init__()
        self.velo = vel
        self.state = state
        img_laser = pygame.image.load('imagens/tiroe.png')
        self.image = pygame.transform.scale(img_laser, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.initial_v = np.array([1, -1])
        self.vel_y_laser = 10
        self.vel_x_laser = 10  # Valor original ajustado para não causar confusão

        self.flag_tiro = True
        self.planetas = planetas
        
        sprites.add(self)
        self.sprites = sprites

        

    def update(self, delta_t):
        # Preciso fazer com que os tiros andem na direção do mouse
        if self.flag_tiro:
            posicao_mouse = pygame.mouse.get_pos()
            posicao_atual = np.array([self.rect.x, self.rect.y])
            mod = np.linalg.norm(posicao_mouse - posicao_atual)
            x = 1 / mod
            nova_v = (posicao_mouse - posicao_atual) * x * 2
            self.initial_v = nova_v
            self.flag_tiro = False
        forca = np.array([0,0])
        for planeta in self.planetas:
            x = planeta.rect.x
            y = planeta.rect.y
            tamanho_vetor_horizontal = x - self.rect.x
            tamanho_vetor_vertical = y - self.rect.y
            vetor = np.array([tamanho_vetor_horizontal, tamanho_vetor_vertical])
            vetor  = vetor / np.linalg.norm(vetor)
            forca = vetor*(5000/ (tamanho_vetor_horizontal**2 + tamanho_vetor_vertical**2)**0.5)
            
        # Atualiza a posição com base na nova velocidade e aceleração
        self.rect.x += self.initial_v[0] + forca[0]/100
        self.rect.y += self.initial_v[1] + forca[1]/100
        

        # Verifica se o tiro saiu da tela ou atingiu um planeta
        if self.rect.x > 800 or self.rect.y > 600 or self.rect.y < 0:
            self.flag_tiro = True
            self.sprites.remove(self)
    
        lista = pygame.sprite.spritecollide(self, self.planetas, True)
        if self.state["flag_tela2"]:
            for planeta in lista:
                self.sprites.remove(self)
                self.planetas.empty()
                self.state["flag_tela2"] = False
        else:
            for planeta in lista:
                self.planetas.empty()
                self.flag_tiro = True
                self.state["flag_tela2"] = True

class Planeta(pygame.sprite.Sprite):
    def __init__(self, sprites, planetas, x, y):
        pygame.sprite.Sprite.__init__(self)

        img_planeta1 = pygame.image.load("imagens/planeta1.png")
        image1 = pygame.transform.scale(img_planeta1,(128,128))
        img_planeta2 = pygame.image.load("imagens/planeta2.png")
        image2 = pygame.transform.scale(img_planeta2,(128,128))
        lista_planetas = [image1, image2]
        self.image = lista_planetas[randint(0,1)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
        planetas.add(self)

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
        fonte = pygame.font.get_default_font()
        fonte = pygame.font.Font(fonte, 24)
        self.window.fill((255,255,255))
        self.texto = fonte.render("clique em qualquer botao", True, (0,0,0))
        
        self.window.blit(self.texto, (200, 240))
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
        fonte = pygame.font.get_default_font()
        fonte = pygame.font.Font(fonte, 24)
        self.window.fill((255,255,255))
        self.texto = fonte.render("Você perdeu", True, (0,0,0))
        self.window.blit(self.texto, (260, 240))
        pygame.display.update()

