
from random import randint
import pygame
import numpy as np
import math
from assets import *
from state import *
from funcoes import *


class Jogo: #Classe que gera o jogo
    def __init__(self):
        # Define as variáveis do jogo
        self.sprites = pygame.sprite.Group()
        self.alvo = pygame.sprite.Group()
        self.planeta = pygame.sprite.Group()

        self.window = Jogo.inicializa(self)
        self.jogador = Jogador(self.alvo)

        self.fonte = assets["fonte_padrao"]
        self.fonte_titulo = pygame.font.Font(self.fonte, 32)

        estrelas = Estrela(50) # Gera 50 estrelas
        self.lista_estrelas = estrelas.gera_estrelas()

        coord_alvo = assets["coord_alvo_1"]
        for i in range(len(coord_alvo)): # Cria um alvo nas coordenadas especificadas
            Alvo(self.sprites, self.alvo, coord_alvo[i][0], coord_alvo[i][1])

        coord_planeta = assets["coord_planetas_1"]
        for i in range(len(coord_planeta)): # Cria um planeta nas coordenadas especificadas
            Planeta(self.sprites, self.planeta, coord_planeta[i][0], coord_planeta[i][1])
        
        self.sprites.add(self.jogador)
        self.fonte = pygame.font.Font(assets["fonte_padrao"], 12)
        self.tela = "tela_inicial"
        self.flag_tiro = False
        self.vel = 1.0
        self.window = assets["window"]
        self.fonte_vel = pygame.font.Font(assets["fonte_padrao"],20)
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
                pos = pygame.mouse.get_pos() #Atira apenas se o mouse estiver perto da nave onde a "mira" está
                if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:
                    Tiro(self.sprites, self.alvo, self.jogador, self.jogador.rect.x + 100, self.jogador.rect.y + 40, self.vel, self.planeta)
                    piu_piu = carregar_audio("musicas\_Piu Piu Disparo_ Efecto de Sonido.mp3")
                    reproduzir_audio(piu_piu, duracao=650)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e: #Aumenta a velocidade do tiro
                if self.vel < 3.0:
                    self.vel = self.vel + 0.3

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >= 1.3 :
                    self.vel -= 0.3
                    
        last_update(self)
        return "tela_jogo"

    def inicializa(self):
        pygame.init()
        # Inicializa a janela
        self.window = assets["window"]
        # Define o título da janela
        pygame.display.set_caption("Ovni Wars")

        if not(assets["musica_tocando"]):
            assets["musica_tocando"] = True
        return self.window
    
    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(assets["fundo"], (0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        #Mosta na tela o FPS
        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))

        # Mostra na tela o Multiplicador de velocidade do tiro
        self.velocidade = f"{self.vel}".split("0")

        contorno(self,f"Multiplicador de velocidade: {self.velocidade[0]}0x",self.fonte_vel,(255,255,255),5,10,(0,0,0))

       #Desenha a mira se o mouse estiver perto da nave
        pos = pygame.mouse.get_pos()
        if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:  
            mouse_pos = pygame.mouse.get_pos() 
            y_jogador = self.jogador.rect.centery
            if mouse_pos[1] < y_jogador:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +85.5), (pos[0], pos[1]))
            else:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +86.5), (pos[0], pos[1]))
        
        self.sprites.draw(self.window)
        pygame.display.update()
    
    def game_loop(self): #Loop do jogo
        # Dicionário de telas
        telas = {
            "tela_inicial": TelaInicial(self.window, self.tela),
            "tela_jogo": self,
            "tela_jogo2": TelaJogo2(self.window, self.tela),
            "tela_over": TelaGameOver(self.window, self.tela),
            "tela_jogo3": TelaJogo3(self.window, self.tela),
            "tela_jogo4": TelaJogo4(self.window, self.tela)
        }

        tela_atual = telas[self.tela]
        while True: 
            self.tela = tela_atual.recebe_eventos()
            if self.tela == False:
                break
            if state["flag_tela2"]:
                self.tela = "tela_jogo2"
            if state["flag_tela3"]:
                self.tela = "tela_jogo3"
            if state["flag_tela4"]:
                self.tela = "tela_jogo4"
            # Atualiza a tela atual
            tela_atual = telas[self.tela]
            tela_atual.desenha()

class TelaJogo2: #Classe que gera a segunda tela do jogo
    def __init__(self, window, tela):      
        # Define as variáveis da tela 2
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
        self.vel = 1.0
        self.window = window 

        self.fonte_vel = pygame.font.Font(assets["fonte_padrao"],20)
       

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
                pos = pygame.mouse.get_pos()
                if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:
                    piu_piu = carregar_audio("musicas\_Piu Piu Disparo_ Efecto de Sonido.mp3")
                    reproduzir_audio(piu_piu, duracao=650)
                    Tiro(self.sprites, self.alvo, self.jogador, self.jogador.rect.x + 100, self.jogador.rect.y + 40, self.vel, self.planeta)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.0:
                    self.vel += 0.3             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >= 1.3 :
                    self.vel -= 0.3

        last_update(self)
        return "tela_jogo2"

    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(assets["fundo2"], (0,0))

        self.velocidade = f"{self.vel}".split("0")
        contorno(self,f"Multiplicador de velocidade: {self.velocidade[0]}0x",self.fonte_vel,(255,255,255),5,10,(0,0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))
        
        pos = pygame.mouse.get_pos()
        if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:  
            mouse_pos = pygame.mouse.get_pos() 
            y_jogador = self.jogador.rect.centery
            if mouse_pos[1] < y_jogador:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +85.5), (pos[0], pos[1]))
            else:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +86.5), (pos[0], pos[1]))
        self.sprites.draw(self.window)
        pygame.display.update()

class TelaJogo3: #Classe que gera a terceira tela do jogo
    def __init__(self, window, tela):   
        # Define as variáveis da tela 3   
        self.sprites = pygame.sprite.Group()
        self.alvo = pygame.sprite.Group()
        self.planeta = pygame.sprite.Group()

        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()

        self.jogador = Jogador(self.alvo)
        self.sprites.add(self.jogador)

        coord_alvo = assets["coord_alvo_3"]
        Alvo(self.sprites, self.alvo, coord_alvo[0][0], coord_alvo[0][1])

        coord_planeta = assets["coord_planetas_3"]
        for i in range(len(coord_planeta)):
            Planeta(self.sprites, self.planeta, coord_planeta[i][0], coord_planeta[i][1])  
        
        self.fonte = pygame.font.Font(assets["fonte_padrao"], 12)
        self.tela = tela
        
        self.flag_tiro = False
        self.vel = 1.0
        self.window = window 

        self.fonte_vel = pygame.font.Font(assets["fonte_padrao"],20)

    def recebe_eventos(self):
        velocidade = 400
        for event in pygame.event.get():
            if event.type == pygame.QUIT or state["flag_tela3"] == False:
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
                pos = pygame.mouse.get_pos()
                if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:
                    Tiro(self.sprites, self.alvo, self.jogador, self.jogador.rect.x + 100, self.jogador.rect.y + 40, self.vel, self.planeta)
                    piu_piu = carregar_audio("musicas\_Piu Piu Disparo_ Efecto de Sonido.mp3")
                    reproduzir_audio(piu_piu, duracao=650)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.0:
                    self.vel += 0.3             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >= 1.3 :
                    self.vel -= 0.3
        last_update(self)
        return "tela_jogo3"

    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(assets["fundo3"], (0,0))


        self.velocidade = f"{self.vel}".split("0")
        contorno(self,f"Multiplicador de velocidade: {self.velocidade[0]}0x",self.fonte_vel,(255,255,255),5,10,(0,0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))

        pos = pygame.mouse.get_pos()
        if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:  
            mouse_pos = pygame.mouse.get_pos() 
            y_jogador = self.jogador.rect.centery
            if mouse_pos[1] < y_jogador:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +85.5), (pos[0], pos[1]))
            else:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +86.5), (pos[0], pos[1]))

        self.sprites.draw(self.window)
        pygame.display.update()

class TelaJogo4: #Classe que gera a quarta tela do jogo
    def __init__(self, window, tela):
        # Define as variáveis da tela 4      
        self.sprites = pygame.sprite.Group()
        self.alvo = pygame.sprite.Group()
        self.planeta = pygame.sprite.Group()

        estrelas = Estrela(50)
        self.lista_estrelas = estrelas.gera_estrelas()

        self.jogador = Jogador(self.alvo)
        self.sprites.add(self.jogador)

        coord_alvo = assets["coord_alvo_4"]
        Alvo(self.sprites, self.alvo, coord_alvo[0][0], coord_alvo[0][1])

        coord_planeta = assets["coord_planetas_4"]
        for i in range(len(coord_planeta)):
            Planeta(self.sprites, self.planeta, coord_planeta[i][0], coord_planeta[i][1])

        self.fonte = pygame.font.Font(assets["fonte_padrao"], 12)
        self.tela = tela
        
        self.flag_tiro = False
        self.vel = 1.0
        self.window = window 

    def recebe_eventos(self):
        velocidade = 400
        for event in pygame.event.get():
            if event.type == pygame.QUIT or state["flag_tela4"] == False:
                pygame.mixer.stop() 
                self.musica_fundo = carregar_audio("musicas/fundo_win.mp3")
                reproduzir_fundo(self.musica_fundo, loop = True)
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
                pos = pygame.mouse.get_pos()
                if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:
                    Tiro(self.sprites, self.alvo, self.jogador, self.jogador.rect.x + 100, self.jogador.rect.y + 40, self.vel, self.planeta)
                    piu_piu = carregar_audio("musicas\_Piu Piu Disparo_ Efecto de Sonido.mp3")
                    reproduzir_audio(piu_piu, duracao=650)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.vel < 3.0:
                    self.vel += 0.3             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self.vel >= 1.3 :
                    self.vel -= 0.3
        last_update(self)
        return "tela_jogo4"

    def desenha(self):
        self.window.fill((0,0,0))
        self.window.blit(assets["fundo4"], (0,0))

        self.fonte_vel = pygame.font.Font(assets["fonte_padrao"],20)
        self.velocidade = f"{self.vel}".split("0")

        contorno(self,f"Multiplicador de velocidade: {self.velocidade[0]}0x",self.fonte_vel,(255,255,255),5,10,(0,0,0))

        for cada_lista in self.lista_estrelas:
            pygame.draw.circle(self.window,(255,255,255), (cada_lista[0],cada_lista[1]), cada_lista[2])

        w, h = pygame.display.get_surface().get_size()
        texto_fps = fps(self)
        self.window.blit(texto_fps,(w - 130,h - 20))

        pos = pygame.mouse.get_pos()
        if pos[0] < 250 and pos[1] < self.jogador.rect.y + 200 and pos[1] > self.jogador.rect.y - 100:  
            mouse_pos = pygame.mouse.get_pos() 
            y_jogador = self.jogador.rect.centery
            if mouse_pos[1] < y_jogador:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +85.5), (pos[0], pos[1]))
            else:
                pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 80,self.jogador.rect.y +86.5), (pos[0], pos[1]))
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
        #Calcula o ângulo da nave em relação ao mouse e rotaciona a imagem
        mouse_pos = pygame.mouse.get_pos() 
        self.angle = math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx)
        self.image = pygame.transform.rotate(self.image_original, math.degrees(-self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        #Nave pode andar para cima e para baixo
        self.rect.y = (self.rect.y + self.vel_y*delta_t)
        if self.rect.y + self.rect.height >= 600:
            self.rect.y = 600 - self.rect.height
        if self.rect.y < 0:
            self.rect.y = 0


class Planeta(pygame.sprite.Sprite):
    def __init__(self, sprites, planeta,  x, y):
        pygame.sprite.Sprite.__init__(self)
        # Define as variáveis do planeta
        imagens = [assets["img_planeta1"], assets["img_planeta2"], assets["img_planeta3"], assets["img_planeta4"]]
        self.image = imagens[randint(0,3)] # Escolhe uma imagem de forma aleatória
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
        planeta.add(self)

class Tiro(pygame.sprite.Sprite):
    def __init__(self, sprites, alvo, jogador, x, y, vel, planeta):
        super().__init__()
        # Define as variáveis do tiro
        self.velo = vel
        self.planetas = planeta
        self.alvo = alvo
        self.original_image = assets["img_tiro"]
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = np.array([0, 0])
        self.flag_tiro = True
        sprites.add(self)
        self.sprites = sprites

    def update(self, delta_t):
        if self.flag_tiro:
            posicao_mouse = pygame.mouse.get_pos()
            posicao_mouse = np.array([posicao_mouse[0], posicao_mouse[1]])
            posicao_atual = np.array([self.rect.x, self.rect.y])
            vetor = posicao_mouse - posicao_atual # Vetor que aponta para a posição do mouse
            mod = np.linalg.norm(vetor) # Módulo do vetor
            vetor_norm = vetor / mod # Vetor normalizado
            self.velocidade = vetor_norm * 4 
            self.flag_tiro = False
      
        C = 4000 # Constante de aceleração
        aceleracao_final = np.array([0.0, 0.0])  
        for planeta in self.planetas:
            # Encontra o centro do planeta pois a imagem é 100x100
            centro_x = planeta.rect.x + 50
            centro_y = planeta.rect.y + 50
            # Calcula a distância entre o tiro e o centro do planeta
            distancia = np.sqrt((self.rect.x - centro_x)**2 + (self.rect.y - centro_y)**2)
            # Calcula a aceleração 
            aceleracao = C / (distancia**2)
            # Calcula o vetor que aponta para o centro do planeta e normaliza
            vetor = np.array([centro_x - self.rect.x, centro_y - self.rect.y])
            vetor_normalizado = vetor / np.linalg.norm(vetor)
            # Multiplica o vetor normalizado pela aceleração
            aceleracao*=vetor_normalizado
            aceleracao_final += aceleracao

            #Verifica se o tiro colidiu com o planeta
            if abs(centro_x - self.rect.x) < 40 and abs(self.rect.y - centro_y) < 40:
                self.kill()
        # Atualiza a velocidade e a posição do tiro
        self.velocidade += aceleracao_final * self.velo
        self.rect.x += self.velocidade[0] 
        self.rect.y += self.velocidade[1]

        #Quando está na tela X,  a flag_telaX é setada para True
        if state["flag_tela2"] == False: #Entra se está na tela_jogo
            lista = pygame.sprite.spritecollide(self, self.alvo, True)
            for alvo in lista:#Verifica se o tiro colidiu com o alvo
                self.sprites.remove(self)
                state["flag_tela2"] = True
        elif state["flag_tela3"] == False: #Entra se está na tela_jogo2
            lista = pygame.sprite.spritecollide(self, self.alvo, True)
            for alvo in lista:
                self.sprites.remove(self)
                state["flag_tela3"] = True
        elif state["flag_tela4"] == False: #Entra se está na tela_jogo3
            lista = pygame.sprite.spritecollide(self, self.alvo, True)
            for alvo in lista:
                self.sprites.remove(self)
                state["flag_tela4"] = True
        else: #Entra se está na tela_jogo4
            lista = pygame.sprite.spritecollide(self, self.alvo, True)
            for alvo in lista:
                self.sprites.remove(self)
                state["flag_tela4"] = False
                state["flag_tela3"] = False
                state["flag_tela2"] = False
        #Se o tiro sair da tela, ele é removido
        if self.rect.x > 790 or self.rect.x < 0 or self.rect.y > 600 or self.rect.y < 0:
            self.kill()

class Alvo(pygame.sprite.Sprite): #Classe que gera o alvo
    def __init__(self, sprites, alvo, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Define as variáveis do alvo
        self.image = assets["img_alvo"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
        alvo.add(self)

class Estrela: #Classe que gera as estrelas
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
    

class TelaInicial: #Classe que gera a tela inicial
    def __init__(self, window, tela):
        # Define as variáveis da tela inicial
        pygame.init()
        self.window = window
        self.tela = tela
        self.musica_fundo = carregar_audio("musicas/fundo_tela_inicial.mp3")
        reproduzir_fundo(self.musica_fundo, loop = True)
        
    def recebe_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pygame.mixer.stop() 
                self.musica_fundo_jogo = carregar_audio("musicas/fundo_jogo.mp3")
                reproduzir_fundo(self.musica_fundo_jogo, loop = True)
                return "tela_jogo"
        return "tela_inicial"
    
    def desenha(self):
        fonte = assets["fonte_padrao"]
        fonte_titulo = pygame.font.Font(fonte, 60)
        fonte_24 = pygame.font.Font(fonte, 24)
        fonte_30 = pygame.font.Font(fonte, 30)
        fonte = pygame.font.Font(fonte, 40)

        fundo = assets["fundo_inicial"]
        self.window.blit(fundo, (0,0))

        contorno(self, "Ovni Wars", fonte_titulo, (0,0,139),250,75, (255,255,255))

        contorno(self, "Aperte (BARRA)", fonte, (255,0,0),250,201,(0,0,0))
        contorno(self, "para iniciar", fonte, (255,0,0),285,241,(0,0,0))

        contorno(self, "Instruções:", fonte_30, (255,255,0),330,360,(0,0,0))

        contorno(self, "(Q) para diminuir a", fonte_24,(255,255,255) ,160,400,(0,0,0))
        contorno(self, "velocidade do tiro", fonte_24,(255,255,255) ,160,425,(0,0,0))
        contorno(self,"(E) para aumentar a",fonte_24,(255,255,255),160,460,(0,0,0))
        contorno(self,"velocidade do tiro",fonte_24,(255,255,255),160,485,(0,0,0))
        contorno(self,"(CIMA)(BAIXO) para ",fonte_24,(255,255,255),160,525,(0,0,0))
        contorno(self,"mexer a nave",fonte_24,(255,255,255),160,550,(0,0,0))
        
        pygame.draw.line(self.window, (255,255,255), (410,400), (410,600))

        contorno(self,"Aperte (BARRA) para",fonte_24,(255,255,255), 430,400,(0,0,0))
        contorno(self,"atirar",fonte_24,(255,255,255), 430,425,(0,0,0))
        contorno(self, "Mantenha o mouse", fonte_24,(255,255,255) ,430,460,(0,0,0))
        contorno(self,"perto da nave para ",fonte_24,(255,255,255), 430,485,(0,0,0))
        contorno(self,"mirar e atirar",fonte_24,(255,255,255), 430,510,(0,0,0))

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
        return "tela_over"
    
    def desenha(self):
        img = assets["fundo_win"]
        self.window.blit(img, (0,0))
        # Renderiza o texto como uma superfície
        win = assets["win"]
        alvo = assets["img_alvo"]
        alvo = pygame.transform.scale(alvo, (230,230))
        # Define a posição onde o texto será desenhado
        posicao = (800/2 - 300, 600/2 - 125)
        # Desenha o texto na janela
        self.window.blit(win, posicao)
        self.window.blit(alvo, (450, 600/2 - 100))
        pygame.display.update()

