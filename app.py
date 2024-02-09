from importes import *
pygame.init()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Tamanho da tela e definição do FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 60  # Frames por Segundo

canhao = Canhao()
bolas = pygame.sprite.Group()
passaro = Passaro()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Verifica se ocorreu um clique do mouse esquerdo
            # Obtém a posição do mouse
                mouse_pos = pygame.mouse.get_pos()
                print("Posição do mouse:", mouse_pos)
                bola = Bola(canhao.rect.center)  # Cria uma nova bola na posição do canhão
                bolas.add(bola)  # Adiciona a bola à lista de bolas

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Se a tecla pressionada for o "Escape"
                running = False

    canhao.draw()
    passaro.draw()

    for bola in bolas:
        bola.update()
        screen.blit(bola.image, bola.rect)

    pygame.display.flip()  # Atualiza a tela
    clock.tick(FPS)  # Limita o FPS

pygame.quit()  # Finaliza o Pygame
sys.exit()
