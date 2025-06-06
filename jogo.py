import pygame
import random
import os

pygame.init()
pygame.mixer.init()

LARGURA, ALTURA = 1000, 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Defenda o Tesouro")

BRANCO = (255, 255, 255)

def carregar_imagem(nome, tamanho=None):
    caminho = os.path.join(os.path.dirname(__file__), "imagens", nome)
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Imagem não encontrada: {caminho}")
    imagem = pygame.image.load(caminho).convert_alpha()
    if tamanho:
        imagem = pygame.transform.scale(imagem, tamanho)
    return imagem

fundo_img = carregar_imagem("fundo.png", (LARGURA, ALTURA))
jogador_img = carregar_imagem("jogador.png", (30, 50))
inimigo_img = carregar_imagem("inimigo.png", (40, 40))
tesouro_img = carregar_imagem("tesouro.png", (20, 80))

som_tiro = pygame.mixer.Sound(os.path.join("sons", "tiro.wav"))
som_inimigo_morto = pygame.mixer.Sound(os.path.join("sons", "inimigo_morto.wav"))
som_game_over = pygame.mixer.Sound(os.path.join("sons", "game_over.wav"))

jogador = pygame.Rect(50, ALTURA // 2 - 25, 30, 50)
tesouro = pygame.Rect(10, ALTURA // 2 - 40, 20, 80)
balas = []
inimigos = []

vel_jogador = 5
vel_bala = 10
vel_inimigo = 3
intervalo_spawn = 1500
tempo_ultimo_inimigo = pygame.time.get_ticks()
vida_tesouro = 3
pontuacao = 0

fonte = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
rodando = True
while rodando:
    clock.tick(60)
    TELA.blit(fundo_img, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and jogador.top > 0:
        jogador.y -= vel_jogador
    if teclas[pygame.K_DOWN] and jogador.bottom < ALTURA:
        jogador.y += vel_jogador
    if teclas[pygame.K_SPACE]:
        if len(balas) < 5:
            nova_bala = pygame.Rect(jogador.right, jogador.centery - 5, 10, 10)
            balas.append(nova_bala)
            som_tiro.play()

    for bala in balas[:]:
        bala.x += vel_bala
        if bala.x > LARGURA:
            balas.remove(bala)

    agora = pygame.time.get_ticks()
    if agora - tempo_ultimo_inimigo > intervalo_spawn:
        inimigo_y = random.randint(0, ALTURA - 40)
        inimigos.append(pygame.Rect(LARGURA, inimigo_y, 40, 40))
        tempo_ultimo_inimigo = agora

    for inimigo in inimigos[:]:
        inimigo.x -= vel_inimigo
        if inimigo.colliderect(tesouro):
            vida_tesouro -= 1
            inimigos.remove(inimigo)
        for bala in balas[:]:
            if inimigo.colliderect(bala):
                pontuacao += 1
                inimigos.remove(inimigo)
                balas.remove(bala)
                som_inimigo_morto.play()
                break

    TELA.blit(tesouro_img, tesouro)
    TELA.blit(jogador_img, jogador)
    for inimigo in inimigos:
        TELA.blit(inimigo_img, inimigo)
    for bala in balas:
        pygame.draw.rect(TELA, BRANCO, bala)

    texto = fonte.render(f"Pontos: {pontuacao} | Vida do Tesouro: {vida_tesouro}", True, BRANCO)
    TELA.blit(texto, (20, 20))
    pygame.display.flip()

    if vida_tesouro <= 0:
        som_game_over.play()
        rodando = False

TELA.fill((0, 0, 0))
msg = fonte.render(f"Game Over! Pontuação final: {pontuacao}", True, BRANCO)
TELA.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2))
pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()
