
import pygame, random, os, math, datetime
from recursos.funcoes import limparTela, aguarde, reconhecimentoVoz, pc_falar

pygame.init()
pygame.mixer.init()

# --- Configurações da Tela ---
LARGURA, ALTURA = 1000, 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Defenda o Tesouro")

# --- Cores ---
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# --- Função para Carregar Imagens ---
def carregar_imagem(nome, tamanho=None):
    caminho = os.path.join(os.path.dirname(__file__), "recursos", nome)
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Imagem não encontrada: {caminho}")
    imagem = pygame.image.load(caminho).convert_alpha()
    if tamanho:
        imagem = pygame.transform.scale(imagem, tamanho)
    return imagem

# --- Carregamento de Mídia (sem iniciar música ainda) ---
fundo_img = carregar_imagem("fundo.png", (LARGURA, ALTURA))
jogador_img = carregar_imagem("jogador.png", (80, 100))
inimigo_img = carregar_imagem("inimigo.png", (80, 100))
tesouro_img = carregar_imagem("tesouro.png", (50, 80))
erva_daninha_img = carregar_imagem("erva_daninha.png", (60, 60))

coracoes_imgs = [
    carregar_imagem("heart_full.png"),
    carregar_imagem("heart_2_3.png"),
    carregar_imagem("heart_1_3.png"),
    carregar_imagem("heart_empty.png")
]

som_tiro = pygame.mixer.Sound(os.path.join("recursos", "tiro.wav"))
som_inimigo_morto = pygame.mixer.Sound(os.path.join("recursos", "inimigo_morto.wav"))
som_game_over = pygame.mixer.Sound(os.path.join("recursos", "game_over.wav"))
pygame.mixer.music.load(os.path.join("recursos", "tema_do_jogo.wav"))

# Reduzir volume dos sons
som_tiro.set_volume(0.4)
som_inimigo_morto.set_volume(0.4)
som_game_over.set_volume(0.4)
pygame.mixer.music.set_volume(0.3)  # Música só tocará após o menu

# --- Tela Inicial com reconhecimento de voz ---
def mostrar_tela_inicial():
    fonte_grande = pygame.font.SysFont(None, 64)
    fonte_pequena = pygame.font.SysFont(None, 32)
    nome = ""
    aguardando_nome = True
    esperando_comeco = False

    while aguardando_nome:
        TELA.fill((0, 0, 0))
        texto_topo = fonte_grande.render("Digite seu nome", True, BRANCO)
        texto_nome = fonte_grande.render(nome + "|", True, BRANCO)
        texto_voz = fonte_pequena.render('Aperte "G" para falar seu nome', True, BRANCO)

        TELA.blit(texto_topo, (LARGURA // 2 - texto_topo.get_width() // 2, 180))
        TELA.blit(texto_nome, (LARGURA // 2 - texto_nome.get_width() // 2, 260))
        TELA.blit(texto_voz, (LARGURA // 2 - texto_voz.get_width() // 2, 340))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome:
                    aguardando_nome = False
                    esperando_comeco = True
                    pc_falar(f"Bem-vindo, {nome}", voz_grossa=True)
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif evento.key == pygame.K_g:
                    try:
                        pc_falar("Diga seu nome", voz_grossa=True)
                        nome_voz = reconhecimentoVoz().capitalize()
                        if nome_voz:
                            nome = nome_voz
                            pc_falar(f"Bem-vindo, {nome}", voz_grossa=True)
                            aguardando_nome = False
                            esperando_comeco = True
                    except Exception as e:
                        print(f"Erro no reconhecimento de voz: {e}")
                        nome = "Jogador"
                        pc_falar("Bem-vindo, Jogador", voz_grossa=True)
                        aguardando_nome = False
                        esperando_comeco = True
                elif len(nome) < 12:
                    nome += evento.unicode

    while esperando_comeco:
        TELA.fill((10, 10, 10))
        bem_vindo = fonte_grande.render(f"Bem-vindo, {nome}!", True, BRANCO)
        instrucoes = [
            "Defenda o tesouro dos inimigos.",
            "Setas cima/baixo para mover.",
            "Tecla 'F' para atirar.",
            "Aperte ESPAÇO para pausar.",
            "Boa sorte!"
        ]
        for i, linha in enumerate(instrucoes):
            txt = fonte_pequena.render(linha, True, BRANCO)
            TELA.blit(txt, (LARGURA // 2 - txt.get_width() // 2, 250 + i * 40))

        TELA.blit(bem_vindo, (LARGURA // 2 - bem_vindo.get_width() // 2, 150))
        pressione = fonte_pequena.render("Aperte ESPAÇO para começar", True, BRANCO)
        TELA.blit(pressione, (LARGURA // 2 - pressione.get_width() // 2, 500))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando_comeco = False

    # Música só inicia agora
    pygame.mixer.music.play(-1)
    return nome
# --- Log de Partidas ---
def salvar_log(nome_jogador, pontos):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    caminho = os.path.join("logs", "registros.txt")
    agora = datetime.datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(f"{nome_jogador} - Pontos: {pontos} - Data: {data} - Hora: {hora}\n")

def mostrar_ultimos_registros_na_tela(tela, fonte, caminho_log):
    if not os.path.exists(caminho_log):
        return
    with open(caminho_log, "r", encoding="utf-8") as f:
        linhas = f.readlines()[-5:]
    linhas = [linha.strip() for linha in linhas if linha.strip()]
    titulo = fonte.render("Últimos 5 Registros:", True, BRANCO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 + 50))
    for i, linha in enumerate(linhas):
        texto = fonte.render(linha, True, BRANCO)
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 + 90 + i * 30))

# --- Inicialização do Jogo ---
nome_jogador = mostrar_tela_inicial()

jogador = pygame.Rect(125, ALTURA // 2 - jogador_img.get_height() // 2, jogador_img.get_width(), jogador_img.get_height())
tesouro_visual = pygame.Rect(10, ALTURA // 2 - tesouro_img.get_height() // 2, tesouro_img.get_width(), tesouro_img.get_height())
area_colisao_tesouro = pygame.Rect(tesouro_visual.x, 0, tesouro_visual.width, ALTURA)

erva_daninha_rect = erva_daninha_img.get_rect()
erva_daninha_rect.x = random.randint(0, LARGURA - erva_daninha_rect.width)
erva_daninha_rect.y = random.randint(0, ALTURA - erva_daninha_rect.height)
erva_daninha_dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
erva_daninha_dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
tempo_ultima_mudanca_erva = pygame.time.get_ticks()
angulo_erva = 0

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
tempo_inicial = pygame.time.get_ticks()
paused = False
rodando = True

# --- Loop Principal ---
while rodando:
    clock.tick(60)
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido = (tempo_atual - tempo_inicial) / 300

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                paused = not paused
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    if paused:
        TELA.fill((30, 30, 30))
        texto_pausa = fonte.render("JOGO PAUSADO - Aperte espaço para continuar", True, BRANCO)
        TELA.blit(texto_pausa, (LARGURA // 2 - texto_pausa.get_width() // 2, ALTURA // 2))
        pygame.display.flip()
        continue

    TELA.blit(fundo_img, (0, 0))

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and jogador.top > 0:
        jogador.y -= vel_jogador
    if teclas[pygame.K_DOWN] and jogador.bottom < ALTURA:
        jogador.y += vel_jogador
    if teclas[pygame.K_f] and len(balas) < 5:
        nova_bala = pygame.Rect(jogador.right, jogador.centery - 5, 10, 10)
        balas.append(nova_bala)
        som_tiro.play()

    for bala in balas[:]:
        bala.x += vel_bala
        if bala.x > LARGURA:
            balas.remove(bala)

    agora = pygame.time.get_ticks()
    if agora - tempo_ultimo_inimigo > intervalo_spawn:
        inimigo_y = random.randint(0, ALTURA - inimigo_img.get_height())
        inimigos.append(pygame.Rect(LARGURA, inimigo_y, inimigo_img.get_width(), inimigo_img.get_height()))
        tempo_ultimo_inimigo = agora

    for inimigo in inimigos[:]:
        inimigo.x -= vel_inimigo
        if inimigo.colliderect(area_colisao_tesouro) or inimigo.colliderect(jogador):
            vida_tesouro -= 1
            inimigos.remove(inimigo)
        else:
            for bala in balas[:]:
                if inimigo.colliderect(bala):
                    pontuacao += 1
                    inimigos.remove(inimigo)
                    balas.remove(bala)
                    som_inimigo_morto.play()
                    break

    erva_daninha_rect.x += erva_daninha_dx
    erva_daninha_rect.y += erva_daninha_dy

    if erva_daninha_rect.left <= 0 or erva_daninha_rect.right >= LARGURA:
        erva_daninha_dx *= -1
    if erva_daninha_rect.top <= 0 or erva_daninha_rect.bottom >= ALTURA:
        erva_daninha_dy *= -1

    if tempo_atual - tempo_ultima_mudanca_erva > 3000:
        erva_daninha_dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        erva_daninha_dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        tempo_ultima_mudanca_erva = tempo_atual

    angulo_erva += 2
    erva_rotacionada = pygame.transform.rotate(erva_daninha_img, angulo_erva)
    nova_rect = erva_rotacionada.get_rect(center=erva_daninha_rect.center)
    TELA.blit(erva_rotacionada, nova_rect)

    TELA.blit(tesouro_img, tesouro_visual)
    TELA.blit(jogador_img, jogador)
    for inimigo in inimigos:
        TELA.blit(inimigo_img, inimigo)
    for bala in balas:
        pygame.draw.rect(TELA, VERMELHO, bala)

    texto = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    TELA.blit(texto, (20, 20))
    texto_instrucao = fonte.render("Aperte espaço para pausar", True, BRANCO)
    TELA.blit(texto_instrucao, (20, 60))

    if vida_tesouro >= 3:
        coracao_img = coracoes_imgs[0]
    elif vida_tesouro == 2:
        coracao_img = coracoes_imgs[1]
    elif vida_tesouro == 1:
        coracao_img = coracoes_imgs[2]
    else:
        coracao_img = coracoes_imgs[3]

    scale = 1 + 0.05 * math.sin(tempo_decorrido)
    base_size = 100
    scaled_size = int(base_size * scale)
    coracao_animado = pygame.transform.scale(coracao_img, (scaled_size, scaled_size))
    x = LARGURA - scaled_size - 20
    y = 20
    TELA.blit(coracao_animado, (x, y))

    pygame.display.flip()

    if vida_tesouro <= 0:
        som_game_over.play()
        rodando = False
        pygame.mixer.music.stop()

# --- Game Over ---
TELA.fill((0, 0, 0))
msg = fonte.render(f"Game Over! Pontuação final: {pontuacao}", True, BRANCO)
TELA.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2))

salvar_log(nome_jogador, pontuacao)
mostrar_ultimos_registros_na_tela(TELA, fonte, "logs/registros.txt")

pygame.display.flip()
pygame.time.delay(5000)
pygame.quit()

