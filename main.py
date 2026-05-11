import pygame
import random

pygame.init()

# ==============================
# CONFIGURACOES
# ==============================
LARGURA = 1000
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida Fake 3D")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 28)
fonte_menor = pygame.font.SysFont("arial", 22)

# ==============================
# CORES
# ==============================
AZUL_TOPO = (56, 154, 235)
AZUL_BAIXO = (150, 218, 255)
NUVEM = (238, 248, 255)
GRAMA_LONGE = (47, 145, 56)
GRAMA_PERTO = (34, 118, 47)
GRAMA_LINHA = (58, 160, 65)
ASFALTO_ESCURO = (54, 55, 63)
ASFALTO_CLARO = (72, 73, 82)
ASFALTO_LUZ = (92, 93, 102)
BRANCO = (245, 245, 245)
VERMELHO = (220, 22, 24)
VERMELHO_ESCURO = (150, 0, 0)
PRETO = (15, 15, 18)
CINZA_SOMBRA = (20, 20, 24)
AMARELO = (255, 214, 45)
LARANJA = (242, 128, 22)
LARANJA_ESCURO = (185, 72, 10)
VIDRO = (62, 130, 175)
VIDRO_CLARO = (135, 205, 235)

# ==============================
# PISTA
# ==============================
horizonte_y = 140
centro_x = LARGURA // 2
largura_topo = 24
largura_base = 790
num_segmentos = 34
altura_util = ALTURA - horizonte_y
velocidade_scroll = 9
scroll = 0

# Faixas seguras. Elas nao encostam nas bordas da pista.
LANES = [-0.34, 0.0, 0.34]

# ==============================
# CARRO
# ==============================
carro_x = centro_x
carro_y = ALTURA - 72
velocidade_carro = 8

# ==============================
# JOGO
# ==============================
pontuacao = 0
game_over = False
ultimo_lane = None
obstaculos = []


# ==============================
# FUNCOES DE PERSPECTIVA
# ==============================
def profundidade_para_tela(z):
    z = max(0.0, min(1.0, z))
    p = z ** 1.75
    y = horizonte_y + p * altura_util
    largura = largura_topo + (largura_base - largura_topo) * (z ** 2.05)
    return centro_x, y, largura


def largura_pista(z):
    return profundidade_para_tela(z)[2]


def centro_pista(z):
    return centro_x


def limites_pista_base():
    centro, _, largura = profundidade_para_tela(1.0)
    margem = 18
    return centro - largura / 2 + margem, centro + largura / 2 - margem


# ==============================
# OBSTACULOS
# ==============================
def escolher_lane(evitar=None):
    opcoes = [lane for lane in LANES if lane != evitar]
    return random.choice(opcoes)


def criar_obstaculo(z, evitar_lane=None):
    lane = escolher_lane(evitar_lane)
    return {
        "z": z,
        "lane": lane,
        "tipo": random.choice(["cone", "barreira"]),
    }


def criar_obstaculos():
    lista = []
    lane_anterior = None
    for z in [0.09, 0.22, 0.36, 0.52, 0.70]:
        obs = criar_obstaculo(z, lane_anterior)
        lane_anterior = obs["lane"]
        lista.append(obs)
    return lista


obstaculos = criar_obstaculos()


def reciclar_obstaculo(obs):
    global ultimo_lane, pontuacao

    obs["z"] = random.uniform(0.045, 0.095)
    obs["lane"] = escolher_lane(ultimo_lane)
    obs["tipo"] = random.choice(["cone", "barreira", "cone"])
    ultimo_lane = obs["lane"]
    pontuacao += 10


def atualizar_obstaculos():
    velocidade_z = 0.0062 + min(pontuacao, 300) * 0.000004

    for obs in obstaculos:
        obs["z"] += velocidade_z
        if obs["z"] > 1.08:
            reciclar_obstaculo(obs)


# ==============================
# CENARIO
# ==============================
def misturar_cor(c1, c2, t):
    return (
        int(c1[0] * (1 - t) + c2[0] * t),
        int(c1[1] * (1 - t) + c2[1] * t),
        int(c1[2] * (1 - t) + c2[2] * t),
    )


def desenhar_ceu():
    for y in range(horizonte_y):
        t = y / horizonte_y
        pygame.draw.line(tela, misturar_cor(AZUL_TOPO, AZUL_BAIXO, t), (0, y), (LARGURA, y))

    pygame.draw.circle(tela, NUVEM, (135, 52), 18)
    pygame.draw.circle(tela, NUVEM, (162, 45), 25)
    pygame.draw.circle(tela, NUVEM, (194, 54), 17)
    pygame.draw.ellipse(tela, NUVEM, (118, 52, 95, 20))

    pygame.draw.circle(tela, NUVEM, (760, 70), 15)
    pygame.draw.circle(tela, NUVEM, (785, 62), 22)
    pygame.draw.circle(tela, NUVEM, (815, 72), 16)
    pygame.draw.ellipse(tela, NUVEM, (745, 72, 90, 18))


def desenhar_grama():
    for y in range(horizonte_y, ALTURA):
        t = (y - horizonte_y) / altura_util
        pygame.draw.line(tela, misturar_cor(GRAMA_LONGE, GRAMA_PERTO, t), (0, y), (LARGURA, y))

    for i in range(13):
        y = horizonte_y + int((i / 13) ** 1.55 * altura_util)
        pygame.draw.line(tela, GRAMA_LINHA, (0, y), (LARGURA, y), 2)


def desenhar_pista():
    for i in range(num_segmentos):
        z1 = i / num_segmentos
        z2 = (i + 1) / num_segmentos
        c1, y1, w1 = profundidade_para_tela(z1)
        c2, y2, w2 = profundidade_para_tela(z2)

        cor = ASFALTO_CLARO if (i + scroll // 16) % 2 == 0 else ASFALTO_ESCURO

        x1e, x1d = c1 - w1 / 2, c1 + w1 / 2
        x2e, x2d = c2 - w2 / 2, c2 + w2 / 2

        pygame.draw.polygon(tela, cor, [(x1e, y1), (x1d, y1), (x2d, y2), (x2e, y2)])

        acost1 = max(4, w1 * 0.035)
        acost2 = max(7, w2 * 0.035)
        borda_cor = VERMELHO if (i + scroll // 16) % 2 == 0 else BRANCO

        pygame.draw.polygon(tela, borda_cor, [(x1e, y1), (x1e + acost1, y1), (x2e + acost2, y2), (x2e, y2)])
        pygame.draw.polygon(tela, borda_cor, [(x1d - acost1, y1), (x1d, y1), (x2d, y2), (x2d - acost2, y2)])

        sombra1 = max(2, w1 * 0.012)
        sombra2 = max(4, w2 * 0.012)
        pygame.draw.polygon(
            tela,
            (42, 42, 50),
            [(x1e + acost1, y1), (x1e + acost1 + sombra1, y1), (x2e + acost2 + sombra2, y2), (x2e + acost2, y2)],
        )
        pygame.draw.polygon(
            tela,
            (42, 42, 50),
            [(x1d - acost1 - sombra1, y1), (x1d - acost1, y1), (x2d - acost2, y2), (x2d - acost2 - sombra2, y2)],
        )

        if i % 2 == 0:
            faixa1 = max(2, w1 * 0.012)
            faixa2 = max(4, w2 * 0.012)
            pygame.draw.polygon(
                tela,
                BRANCO,
                [(c1 - faixa1 / 2, y1), (c1 + faixa1 / 2, y1), (c2 + faixa2 / 2, y2), (c2 - faixa2 / 2, y2)],
            )

        if i % 5 == 0:
            brilho1 = max(1, w1 * 0.002)
            brilho2 = max(2, w2 * 0.002)
            pygame.draw.polygon(
                tela,
                ASFALTO_LUZ,
                [(c1 - w1 * 0.22, y1), (c1 - w1 * 0.22 + brilho1, y1), (c2 - w2 * 0.22 + brilho2, y2), (c2 - w2 * 0.22, y2)],
            )


# ==============================
# DESENHO DOS PERSONAGENS
# ==============================
def desenhar_carro():
    sombra = pygame.Rect(carro_x - 45, carro_y + 30, 90, 14)
    pygame.draw.ellipse(tela, CINZA_SOMBRA, sombra)

    corpo = pygame.Rect(carro_x - 41, carro_y - 3, 82, 38)
    cabine = pygame.Rect(carro_x - 27, carro_y - 22, 54, 26)
    pygame.draw.rect(tela, VERMELHO, corpo, border_radius=5)
    pygame.draw.rect(tela, (238, 35, 35), cabine, border_radius=5)

    pygame.draw.polygon(
        tela,
        VIDRO,
        [(carro_x - 18, carro_y - 17), (carro_x + 18, carro_y - 17), (carro_x + 24, carro_y + 1), (carro_x - 24, carro_y + 1)],
    )
    pygame.draw.line(tela, VIDRO_CLARO, (carro_x - 12, carro_y - 15), (carro_x + 12, carro_y - 15), 2)

    pygame.draw.rect(tela, PRETO, (carro_x - 37, carro_y + 20, 14, 15), border_radius=3)
    pygame.draw.rect(tela, PRETO, (carro_x + 23, carro_y + 20, 14, 15), border_radius=3)
    pygame.draw.rect(tela, AMARELO, (carro_x - 32, carro_y + 7, 12, 8), border_radius=2)
    pygame.draw.rect(tela, AMARELO, (carro_x + 20, carro_y + 7, 12, 8), border_radius=2)
    pygame.draw.rect(tela, VERMELHO_ESCURO, (carro_x - 38, carro_y + 28, 76, 7), border_radius=3)

    return pygame.Rect(carro_x - 38, carro_y - 18, 76, 50)


def desenhar_cone(x, y, tamanho):
    largura = tamanho * 0.72
    altura = tamanho * 1.12

    pygame.draw.ellipse(tela, CINZA_SOMBRA, (x - largura * 0.55, y + altura * 0.34, largura * 1.1, altura * 0.22))
    rect_colisao = pygame.Rect(int(x - largura / 2), int(y - altura / 2), int(largura), int(altura))

    base = pygame.Rect(int(x - largura * 0.58), int(y + altura * 0.25), int(largura * 1.16), int(altura * 0.18))
    pygame.draw.rect(tela, LARANJA_ESCURO, base, border_radius=3)
    pygame.draw.rect(tela, BRANCO, (base.x + 4, base.y + 3, max(4, base.width - 8), max(2, base.height // 3)), border_radius=2)

    topo = (x, y - altura * 0.48)
    esq = (x - largura * 0.38, y + altura * 0.32)
    dire = (x + largura * 0.38, y + altura * 0.32)
    pygame.draw.polygon(tela, LARANJA, [topo, esq, dire])
    pygame.draw.polygon(tela, (255, 166, 45), [(x, y - altura * 0.42), (x - largura * 0.16, y + altura * 0.22), (x + largura * 0.04, y + altura * 0.22)])
    pygame.draw.polygon(tela, BRANCO, [(x - largura * 0.22, y + altura * 0.02), (x + largura * 0.22, y + altura * 0.02), (x + largura * 0.16, y + altura * 0.14), (x - largura * 0.16, y + altura * 0.14)])

    return rect_colisao.inflate(-int(largura * 0.22), -int(altura * 0.08))


def desenhar_barreira(x, y, tamanho):
    largura = tamanho * 1.15
    altura = tamanho * 0.75

    pygame.draw.ellipse(tela, CINZA_SOMBRA, (x - largura * 0.55, y + altura * 0.32, largura * 1.1, altura * 0.25))
    rect_colisao = pygame.Rect(int(x - largura / 2), int(y - altura / 2), int(largura), int(altura))

    pygame.draw.rect(tela, (35, 35, 40), rect_colisao.move(3, 4), border_radius=3)
    pygame.draw.rect(tela, AMARELO, rect_colisao, border_radius=4)
    pygame.draw.rect(tela, PRETO, rect_colisao, 2, border_radius=4)

    stripe_w = max(5, int(largura * 0.16))
    for i in range(-1, 3):
        x1 = rect_colisao.left + i * stripe_w * 2
        pygame.draw.polygon(
            tela,
            LARANJA_ESCURO,
            [(x1, rect_colisao.bottom), (x1 + stripe_w, rect_colisao.bottom), (x1 + stripe_w * 2, rect_colisao.top), (x1 + stripe_w, rect_colisao.top)],
        )

    return rect_colisao.inflate(-int(largura * 0.12), -int(altura * 0.12))


def desenhar_obstaculo(obs):
    z = obs["z"]
    centro, y, largura = profundidade_para_tela(z)
    x = centro + obs["lane"] * largura
    tamanho = 26 + z * 58

    if obs["tipo"] == "barreira":
        return desenhar_barreira(x, y, tamanho)
    return desenhar_cone(x, y, tamanho)


def desenhar_obstaculos(carro_rect):
    global game_over

    for obs in sorted(obstaculos, key=lambda item: item["z"]):
        rect = desenhar_obstaculo(obs)
        if rect.colliderect(carro_rect):
            game_over = True


# ==============================
# INTERFACE
# ==============================
def mostrar_hud():
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontos, (18, 18))

    fase = "Fase 1: pista reta e obstaculos justos"
    if pontuacao >= 120:
        fase = "Fase 2: mais velocidade, mesma pista estavel"

    texto_fase = fonte_menor.render(fase, True, BRANCO)
    tela.blit(texto_fase, (18, 52))

    if game_over:
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        tela.blit(overlay, (0, 0))

        msg1 = fonte.render("GAME OVER", True, BRANCO)
        msg2 = fonte_menor.render("Aperte R para reiniciar", True, BRANCO)
        tela.blit(msg1, (LARGURA // 2 - msg1.get_width() // 2, 34))
        tela.blit(msg2, (LARGURA // 2 - msg2.get_width() // 2, 68))


def reiniciar():
    global carro_x, pontuacao, game_over, scroll, obstaculos, ultimo_lane

    carro_x = centro_x
    pontuacao = 0
    game_over = False
    scroll = 0
    ultimo_lane = None
    obstaculos = criar_obstaculos()


# ==============================
# LOOP PRINCIPAL
# ==============================
rodando = True
while rodando:
    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and game_over:
                reiniciar()

    teclas = pygame.key.get_pressed()

    if not game_over:
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            carro_x -= velocidade_carro
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            carro_x += velocidade_carro

        scroll = (scroll + velocidade_scroll) % 32
        atualizar_obstaculos()

    desenhar_ceu()
    desenhar_grama()
    desenhar_pista()

    carro_rect = desenhar_carro()
    desenhar_obstaculos(carro_rect)

    esquerda, direita = limites_pista_base()
    if carro_rect.left < esquerda or carro_rect.right > direita:
        game_over = True

    mostrar_hud()
    pygame.display.flip()

pygame.quit()
raise SystemExit
