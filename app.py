# from importes import *
# pygame.init()
# import math

# # Cores
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# COR_PERSONAGEM = (30, 200, 20)

# # Tamanho da tela e definição do FPS

# clock = pygame.time.Clock()
# FPS = 60  # Frames por Segundo
# running = True

# largura = 1000
# altura = 700
# tela = pygame.display.set_mode((largura, altura))

# # Inicializar posicoes
# v = np.array([16, -10])
# s = np.array([SCREEN_WIDTH/5,SCREEN_HEIGHT - 50])
# s1 = np.array([SCREEN_WIDTH/5,SCREEN_HEIGHT - 50])

# # Personagem
# bola = pygame.image.load("imagens/bola_de_canhao.png")  # Tamanho do bola
# bola = pygame.transform.scale(bola, (20,20))

# fundo = pygame.image.load("imagens/fundo.png")
# fundo = pygame.transform.scale(fundo, (1000,700))
# rodando = True

# helicoptero = pygame.image.load("imagens/heli.png")
# helicoptero = pygame.transform.scale(helicoptero, (20,20))

# massa_tiro = 10
# massa_planeta1 = 1000

# flag_clicou = False
# flag_atirou = False

# while running:
#     screen.fill(BLACK)
#     screen.blit(fundo, (0, 0))
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             rodando = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 flag_atirou = True
#                 posicao_mouse = pygame.mouse.get_pos()

#     mouse_presses = pygame.mouse.get_pressed()
#     if mouse_presses[0]:
#         pos = pygame.mouse.get_pos()
#         if pos[0] > 600 and pos[0] < 640 and pos[1]>600 and pos[1]<640:
#             flag_clicou = True
#     if flag_clicou:
#         pygame.draw.polygon(screen, (255,0,0), [(600, 600), (640, 600), (640, 640), (600, 640)])
#     else: 
#         pygame.draw.polygon(screen, (0,255,0), [(600, 600), (640, 600), (640, 640), (600, 640)])
    
#     pygame.draw.polygon(screen, (0,0,255), [(200, 200), (240, 200), (240, 240), (200, 240)])

#     if flag_atirou:
#         mod = np.linalg.norm(posicao_mouse-s)
#         x = 1/mod
#         if flag_clicou:
#             nova_v = (posicao_mouse-s)*x*40
#         else:
#             nova_v = (posicao_mouse-s)*x*20
#         s, v = s, nova_v
#         flag_atirou = False

#     forca = 8000/(math.dist((s[0], s[1]), (220,220))**2)
#     aceleracao = np.array([0, forca])
#     s = s + v+aceleracao

#     pos = pygame.mouse.get_pos()
#     pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH/2,SCREEN_HEIGHT - 50), (pos[0], pos[1]))

#     clock.tick(FPS)  # Limita o FPS

#     # Desenhar bola
#     rect = pygame.Rect(s, (10, 10))  
#     screen.blit(bola, rect)

#     rect = pygame.Rect(s1, (10, 10))  
#     screen.blit(helicoptero, rect)
#     # Update!
#     pygame.display.update()

# pygame.quit()  # Finaliza o Pygame
# sys.exit()




from random import randint
import pygame


class Jogo:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.meteoros = pygame.sprite.Group()
        self.assets, self.state, self.window = Jogo.inicializa(self)
        for i in range(1):
            Meteoro(self.sprites, self.meteoros)
        self.jogador = Jogador(self.meteoros)
        self.sprites.add(self.jogador)
        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()
        self.flag = True

        fonte = pygame.font.get_default_font()
        self.fonte = pygame.font.Font(fonte, 12)

        self.tela = "tela_inicial"
        self.tela_inicial = TelaInicial(self)
        self.tela_final = TelaGameOver(self)

        self.flag_tiro = False
        self.game_loop()
        self.window_i = pygame.display.set_mode((800,600))

        

    def inicializa(self):
        pygame.init()
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Jogo do Edu")
        self.assets = {}
        self.state = {}
       
        self.assets["fundo"] = pygame.image.load("imagens/fundo.png")
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
        # self.state["som"] = pygame.mixer.Sound("assets/snd/pew.wav")
        
        
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

        pygame.display.update()

    def recebe_eventos(self):
        velocidade = 400
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.jogador.vidas == 0:
                self.tela = "tela_over"
                return False
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     self.jogador.vel_x+=velocidade
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            #     self.jogador.vel_x-=velocidade
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.jogador.vel_y-=velocidade
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.jogador.vel_y+=velocidade
            # if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            #     self.jogador.vel_x-=velocidade
            # if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            #     self.jogador.vel_x+=velocidade
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.jogador.vel_y+=velocidade
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.jogador.vel_y-=velocidade
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # som = self.state["som"]
                # som.play()
                Tiro(self.sprites, self.meteoros, self.jogador.rect.x, self.jogador.rect.y+25)
                Tiro(self.sprites, self.meteoros, self.jogador.rect.x+20, self.jogador.rect.y)
                Tiro(self.sprites, self.meteoros, self.jogador.rect.x+45, self.jogador.rect.y+25)

        
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
                    self.desenha()
            if self.tela == "tela_over":
                while self.tela_final.recebe_eventos():
                    self.tela_final.desenha()

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
    def __init__(self, meteoros):
        pygame.sprite.Sprite.__init__(self)

        self.flag_borda = False

        img_nave = pygame.image.load('imagens/heli.png')
        image = pygame.transform.scale(img_nave,(64*1.5,48*1.5))
        angulo = 20
        self.image = pygame.transform.rotate(image, angulo)

        self.rect = self.image.get_rect()
        # self.rect.x = 640/2 - self.rect.width/2
        # self.rect.y = 480 - self.rect.height
        self.rect.x = self.rect.width/5
        self.rect.y = 480 - self.rect.height

        self.vel_x = 0
        self.vel_y = 0

        self.meteoros = meteoros

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
        lista = pygame.sprite.spritecollide(self, self.meteoros,True)
        for i in range(len(lista)):
            self.vidas -= 1


class Tiro(pygame.sprite.Sprite):
    def __init__(self, sprites,meteoros, x, y):
        pygame.sprite.Sprite.__init__(self)

        img_laser = pygame.image.load('imagens/bola_de_canhao.png')
        self.image = pygame.transform.scale(img_laser,(16,12))
        
        self.rect = self.image.get_rect()
        self.vel_y_laser = 0

        self.rect.x = x
        self.rect.y = y
        self.vel_x_laser = +500

        self.flag_tiro = False
        self.meteoros = meteoros
        sprites.add(self) 
        self.sprites = sprites 
    def update(self, delta_t):

        self.rect.x = (self.rect.x + self.vel_x_laser*delta_t)
        lista = pygame.sprite.spritecollide(self, self.meteoros,True)
        for tiro in lista:
            self.sprites.remove(self)

class Meteoro(pygame.sprite.Sprite):
    def __init__(self, sprites, meteoros):
        pygame.sprite.Sprite.__init__(self)

        img_meteoro = pygame.image.load("imagens/passaro.png")
        self.image = pygame.transform.scale(img_meteoro,(32,24))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,640)
        self.rect.y = randint(0,480)
        sprites.add(self)
        meteoros.add(self)

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