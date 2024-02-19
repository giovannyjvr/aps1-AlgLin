
# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COR_PERSONAGEM = (30, 200, 20)

# Tamanho da tela e definição do FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 60  # Frames por Segundo

canhao = Canhao()
bolas = pygame.sprite.Group()
passaro = Passaro()
running = True

# Inicializar posicoes
s0 = np.array([SCREEN_WIDTH/2,SCREEN_HEIGHT - 200])
# v0 = np.array([10, -10])
# a = np.array([0, 0.2])
#Modificado
v0 = np.array([16, -10])
a = np.array([0, 0.2])
v = v0
s = s0
clicou = False
atirou = False
# Personagem
personagem = pygame.Surface((5, 5))  # Tamanho do personagem
personagem.fill(COR_PERSONAGEM)  # Cor do personagem
rodando = True

def criar_bola(bolas):
    bola = Bola()
    bola.rect.x = SCREEN_WIDTH/2,  # Posição X inicial da bola
    bola.rect.y = SCREEN_HEIGHT-100  # Posição Y inicial da bola
    bolas.add(bola)



while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                atirou = True
                pos_mouse = pygame.mouse.get_pos()
                


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

        pos = pygame.mouse.get_pos()
        pygame.draw.line(self.window, (255,255,255), (self.jogador.rect.x + 70,self.jogador.rect.y + 50), (pos[0], pos[1]))
        

    screen.fill(BLACK)
    canhao.draw()
    passaro.draw()

    # if atirou:
    #     # v = v + a
    if atirou:
        mod = np.linalg.norm(pos_mouse-s0)
        x = 1/mod
        # if flag_clicou:
        #     nova_v = (posicao_mouse-s)*x*40
        # else:
        nova_v = (posicao_mouse-self.rect)*x*20
        v = nova_v

        forca = 8000/(math.dist((self.rect[0], self.rect[1]), (220,220))**2)
        aceleracao = np.array([0, forca])
        
        
        self.rect = self.rect + v+aceleracao

        # self.rect.x = (self.rect.x + (self.vel_x_laser+aceleracao)*delta_t)
 
        # lista = pygame.sprite.spritecollide(self, self.planetas,True)
        # for tiro in lista:
        #     self.sprites.remove(self)

    pos = pygame.mouse.get_pos()
    # if pos[0] < 500 and pos[1] > 200 and pos[1] < 700:
    pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH/2,SCREEN_HEIGHT - 200), (pos[0], pos[1]))

    for bola in bolas:
        bola.update()
        screen.blit(bola.image, bola.rect)

    # pygame.display.flip()  # Atualiza a tela
    clock.tick(FPS)  # Limita o FPS

    # Desenhar personagem
    rect = pygame.Rect(s, (10, 10))  # First tuple is position, second is size.
    screen.blit(personagem, rect)

    if clicou:
        pygame.draw.polygon(screen, (255,0,0), [(600, 600), (640, 600), (640, 640), (600, 640)])
    else: 
        pygame.draw.polygon(screen, (0,255,0), [(600, 600), (640, 600), (640, 640), (600, 640)])
    # Update!
    pygame.display.update()
    

pygame.quit()  # Finaliza o Pygame
sys.exit()

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