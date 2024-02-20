from random import randint
import pygame
import numpy as np
import math


class Jogo:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.planetas = pygame.sprite.Group()
        self.assets, self.state, self.window = Jogo.inicializa(self)
        for i in range(3):
            Planeta(self.sprites, self.planetas)
        self.jogador = Jogador(self.planetas)
        self.sprites.add(self.jogador)
        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()
        self.flag = True
        self.vel = 1
        fonte = pygame.font.get_default_font()
        self.fonte = pygame.font.Font(fonte, 12)

        self.tela = "tela_inicial"
        self.tela_inicial = TelaInicial(self)
        self.tela_final = TelaGameOver(self)
        self.tela_2 = TelaJogo2(self)
        self.flag_tiro = False
        self.game_loop()
        self.window_i = pygame.display.set_mode((800,600))

        

    def inicializa(self):
        pygame.init()
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Jogo do Edu")
        self.assets = {}
        self.state = {}
        self.assets["fundo"] = pygame.image.load("imagens/fundo_universo.jpg")
        self.assets["flag_estrela"] = True
        fonte = "font/PressStart2P.ttf"
        self.assets["fonte"] = fonte
        self.assets["musica_tocando"] = False
        # musica = pygame.mixer.Sound("assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg")
        if not(self.assets["musica_tocando"]):
            # musica.play()
            self.assets["musica_tocando"] = True
        self.assets["tela"] = "tela_inicial"
        self.state["t0"] = 0
        self.state["vel_nave"] = [0,0]
        self.state["posicao_nave"] = [300,400]
        self.state["last_updated"] = 0
        self.state["flag_tela2"] = False
        return self.assets,self.state, self.window
    
    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(self.assets["fundo"], (0,0))


        fonte = self.assets["fonte"]
        fonte = pygame.font.Font(fonte,12)
        
        coracao = fonte.render(chr(9829) * self.jogador.vidas, True, (255,0,0))
        self.window.blit(coracao, (0,5))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        fps = 0
        t0 = self.state["t0"]
        t1 = pygame.time.get_ticks()
        if t0 > 0:
            fps = 1000/(t1 - t0)
        self.state["t0"] = t1
        texto_fps = fonte.render(f'fps: {fps:.2f}', True, (255,255,255))
        self.window.blit(texto_fps,(w - 130,h - 20))
        self.sprites.draw(self.window)
        posicao_mouse = pygame.mouse.get_pos()
        limite_x = 300
        if posicao_mouse[0] < limite_x:
            # posicao_mouse_y = posicao_mouse[1]
            # posicao_mouse =  (posicao_mouse[0] //5, posicao_mouse[1] //10)
            pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 50,self.jogador.rect.y + 25), posicao_mouse)
        pygame.display.update()


    def recebe_eventos(self):
        velocidade = 400
        if self.state["flag_tela2"]:
            self.tela = "tela_jogo2"
            return False
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
                Tiro(self.sprites, self.planetas,self.jogador, self.jogador.rect.x+50, self.jogador.rect.y+25,self.vel,self.tela, self.state)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.0:
                    self.vel += 0.1
                    print(self.vel)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >0.4 :
                    self.vel -= 0.1
                    print(self.vel)
                
        
        ultimo_tempo = self.state["last_updated"]
        tempo = pygame.time.get_ticks()
        delta_t = (tempo-ultimo_tempo)/1000
        self.state["last_updated"] = tempo
        self.sprites.update(delta_t)
        
        return True
     

    def game_loop(self):
            if self.tela == "tela_inicial":
                while self.tela_inicial.recebe_eventos():
                    self.tela_inicial.desenha()
            if self.tela == "tela_jogo":
                while self.recebe_eventos():
                    tempo_atual = pygame.time.get_ticks()
                    delta_t = (tempo_atual - self.state["last_updated"]) / 1000
                    for planeta in self.planetas:
                        planeta.update(delta_t)
                    self.state["last_updated"] = tempo_atual
                    self.desenha()

            if self.tela == "tela_jogo2":
                print(2)
                self.state["flag_tela2"] = False
                while self.recebe_eventos():
                    self.tela_2.desenha()
            if self.tela == "tela_over":
                while self.tela_final.recebe_eventos():
                    self.tela_final.desenha()

class TelaJogo2:
    def __init__(self, tela):
        pygame.init()
        self.window = pygame.display.set_mode((800,600))
        self.tela = tela
    def desenha(self):
        self.window.fill((0,0,0))
        pygame.display.update()

class TelaInicial:
    def __init__(self,tela):
        pygame.init()
        self.window = pygame.display.set_mode((800,600))
        self.tela = tela

    def recebe_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                self.tela.tela = "tela_jogo"
                return False
        return True
    def desenha(self):
        fonte = pygame.font.get_default_font()
        fonte = pygame.font.Font(fonte, 24)
        self.window.fill((255,255,255))
        self.texto = fonte.render("clique em qualquer botao", True, (0,0,0))
        
        self.window.blit(self.texto, (200, 240))
        pygame.display.update()

class TelaGameOver:
    def __init__(self,tela):
        pygame.init()
        self.window = pygame.display.set_mode((800,600))
        self.tela = tela

    def recebe_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                self.tela.tela = "tela_jogo"
                return False
        return True
    
    def desenha(self):
        fonte = pygame.font.get_default_font()
        fonte = pygame.font.Font(fonte, 24)
        self.window.fill((255,255,255))
        self.texto = fonte.render("Você perdeu", True, (0,0,0))
        self.window.blit(self.texto, (260, 240))
        pygame.display.update()


class Jogador(pygame.sprite.Sprite):
    def __init__(self, planetas):
        pygame.sprite.Sprite.__init__(self)

        self.flag_borda = False
        img_nave = pygame.image.load('imagens/nave.png')
        image = pygame.transform.scale(img_nave,(64,48))
        angulo = 0
        self.image = pygame.transform.rotate(image, angulo)

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width/5
        self.rect.y = 480 - self.rect.height

        self.vel_x = 0
        self.vel_y = 0
        self.planetas = planetas
        self.vidas = 3


    def update(self, delta_t):

        self.rect.x = (self.rect.x + self.vel_x*delta_t) 
        self.rect.y = (self.rect.y + self.vel_y*delta_t)
    
        if self.rect.x + self.rect.width >= 640:
            self.rect.x = 640 - self.rect.width
        if self.rect.x  < 0:
            self.rect.x = 0
        if self.rect.y + self.rect.height >= 600:
            self.rect.y = 600 - self.rect.height
        if self.rect.y < 0:
            self.rect.y = 0
        lista = pygame.sprite.spritecollide(self, self.planetas,True)
        for i in range(len(lista)):
            self.vidas -= 1



class Tiro(pygame.sprite.Sprite):
    def __init__(self, sprites, planetas, jogador, x, y, vel, tela,state):
        super().__init__()
        self.tela = tela
        self.velo = vel
        self.state = state
        img_laser = pygame.image.load('imagens/bola_de_canhao2.png')
        self.image = pygame.transform.scale(img_laser, (16, 12))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.initial_v = np.array([16, -10])
        self.vel_y_laser = 10
        self.vel_x_laser = 10  # Valor original ajustado para não causar confusão

        self.flag_tiro = False
        self.planetas = planetas
        sprites.add(self)
        self.sprites = sprites

        self.flag_tiro = True

    def update(self, delta_t):
        #Preciso fazer com que os tiros andem na direção do mouse
        if self.flag_tiro:
            posicao_mouse = pygame.mouse.get_pos()
            print(posicao_mouse)
            posicao_atual = np.array([self.rect.x, self.rect.y])
            mod = np.linalg.norm(posicao_mouse - posicao_atual)
            x = 1 / mod
            nova_v = (posicao_mouse - posicao_atual) * x * 2
            self.initial_v = nova_v
            self.flag_tiro = False

        self.rect.x += self.initial_v[0] * self.vel_x_laser
        self.rect.y += self.initial_v[1] * self.vel_y_laser
        
        # Atualiza a posição do tiro
        self.rect.x += self.initial_v[0] * self.velo
        self.rect.y += self.initial_v[1] * self.velo
        # print(self.initial_v)
        # Calcula a aceleração
        # a = np.array([0, 8000/(math.dist((self.rect.x, self.rect.y), (220,220))**2)])
        # self.initial_v = self.initial_v 

        # Atualiza a posição com base na nova velocidade e aceleração
        self.rect.x += 0.005 * self.initial_v[0] * self.velo
        self.rect.y += 0.005 * self.initial_v[1] * self.velo
       

        # Verifica se o tiro saiu da tela ou atingiu um planeta
        if self.rect.x > 800 or self.rect.y > 600 or self.rect.y < 0:
            self.flag_tiro = True
            self.sprites.remove(self)
           

        lista = pygame.sprite.spritecollide(self, self.planetas, True)
        for planeta in lista:
            self.sprites.remove(self)
            self.flag_tiro = True
            # self.tela.tela = "tela_jogo2"
            self.state["flag_tela2"] = True
            
                        

class Planeta(pygame.sprite.Sprite):
    def __init__(self, sprites, planetas):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_planetas = ["imagens/planetas/1.png",
                                "imagens/planetas/2.png",
                                "imagens/planetas/3.png",
                                "imagens/planetas/4.png",
                                "imagens/planetas/5.png",
                                "imagens/planetas/6.png",
                                "imagens/planetas/7.png",
                                "imagens/planetas/8.png"]  # Lista de imagens dos planetas
        self.indice_imagem = 0  # Índice da imagem atual
        self.tempo_anterior = pygame.time.get_ticks()  # Tempo da última atualização
        self.image = pygame.image.load(self.imagens_planetas[self.indice_imagem])
        self.image = pygame.transform.scale(self.image, (64, 48))
        self.rect = self.image.get_rect()
        self.rect.x = randint(400, 700)
        self.rect.y = randint(20, 480)
        sprites.add(self)
        planetas.add(self)

    def update(self, delta_t):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_anterior >= 500:  # 2 segundos em milissegundos
            self.indice_imagem = (self.indice_imagem + 1) % len(self.imagens_planetas)  # Próxima imagem na lista
            self.image = pygame.image.load(self.imagens_planetas[self.indice_imagem])  # Atualiza a imagem do planeta
            self.image = pygame.transform.scale(self.image, (64, 48))
            self.tempo_anterior = tempo_atual  # Atualiza o tempo da última atualização


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