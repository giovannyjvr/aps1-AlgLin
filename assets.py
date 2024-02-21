import pygame

assets = {
    "fonte_padrao": pygame.font.get_default_font(),
    "window": pygame.display.set_mode((800,600)),
    "fundo_inicial": pygame.transform.scale(pygame.image.load("imagens/fundo_inicial.jpg"), (800,600)),
    "fundo_final": pygame.transform.scale(pygame.image.load("imagens/fundo_final.jpg"), (800,600)),
    "fundo": pygame.transform.scale(pygame.image.load("imagens/fundo.png"), (800,600)),
    "fundo2": pygame.transform.scale(pygame.image.load("imagens/fundo2.png"), (800,600)),
    "img_nave": pygame.transform.scale(pygame.image.load('imagens/navepft.png'), (100, 100)),
    "img_planeta1": pygame.transform.scale(pygame.image.load("imagens/planeta1.png"),(128,128)),
    "img_planeta2": pygame.transform.scale(pygame.image.load("imagens/planeta2.png"),(128,128)),
    "img_tiro": pygame.transform.scale(pygame.image.load('imagens/tiroe.png'), (50, 50)),
    "img_alvo": pygame.transform.scale(pygame.image.load("imagens/alvo.png"),(100,100)),
    "flag_estrela": True,
    "fonte": "font/PressStart2P.ttf",
    "musica_tocando": False,
    "tela": "tela_inicial",
    "coord_alvo_1": [[600, 400]],
    "coord_planetas_1": [[400, 400]],
    "coord_alvo_2": [[650, 250]],
    "coord_planetas_2": [[300, 300], [500, 200]]
    

}