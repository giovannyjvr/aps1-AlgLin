from importes import *
pygame.init()

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
s0 = np.array([SCREEN_WIDTH/2,SCREEN_HEIGHT - 50])
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
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                atirou = True
                


    mouse_presses = pygame.mouse.get_pressed()
    if mouse_presses[0]:
        pos = pygame.mouse.get_pos()
        if pos[0] > 600 and pos[0] < 640 and pos[1]>600 and pos[1]<640:
            clicou = True

    if s[0]<10 or s[0]>780 or s[1]<10 or s[1]>780: # Se eu chegar ao limite da tela, reinicio a posição do personagem
        y = pygame.mouse.get_pos()
        mod = np.linalg.norm(y-s0)
        # atirou = False
        
        x = 1/mod
        if clicou:
            y = (y-s0)*x*40
        else:
            y = (y-s0)*x*20
        
        
        s, v = s0, y 
        

    screen.fill(BLACK)
    canhao.draw()
    passaro.draw()
  


    # if s[0] < 350 and s[1] < 700:
    pos = pygame.mouse.get_pos()
    # if pos[0] < 500 and pos[1] > 200 and pos[1] < 700:
    pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH/2,SCREEN_HEIGHT - 50), (pos[0], pos[1]))

    

    for bola in bolas:
        bola.update()
        screen.blit(bola.image, bola.rect)

    # pygame.display.flip()  # Atualiza a tela
    clock.tick(FPS)  # Limita o FPS

    if atirou:
        # v = v + a
        s = s + v
        if s[1] < 0:
            atirou = False

    
    
   

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

