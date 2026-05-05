import pygame
import sys
import random

pygame.init()

# ==============================
# CONFIGURAÇÕES
# ==============================
LARGURA = 1000
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida Fake 3D")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 28)
fonte_menor = pygame.font.SysFont("arial", 22)

# ==============================
# CORES
# ==============================
AZUL_TOPO = (70, 170, 255)
AZUL_BAIXO = (120, 210, 255)
VERDE = (40, 140, 40)
CINZA_1 = (65, 65, 75)
CINZA_2 = (85, 85, 95)
BRANCO = (255, 255, 255)
VERMELHO = (220, 0, 0)
PRETO = (0, 0, 0)
AMARELO = (255, 220, 0)
LARANJA = (255, 140, 0)

# ==============================
# PISTA
# ==============================
horizonte_y = 140
centro_x = LARGURA // 2
largura_base_topo = 20
largura_base_baixo = 820
num_faixas = 30
altura_util = ALTURA - horizonte_y
faixa_h = altura_util / num_faixas
scroll = 0
velocidade_scroll = 10

# ==============================
# CARRO
# ==============================
carro_x = centro_x
carro_y = ALTURA - 78
velocidade_carro = 8

# ==============================
# JOGO
# ==============================
pontuacao = 0
game_over = False

# ==============================
# OBSTÁCULOS FIXOS NA PISTA
# lane: -0.45 esquerda | 0 centro | 0.45 direita
# z: profundidade (0 longe / 1 perto)
# ==============================
obstaculos = []

def criar_obstaculos_iniciais():
    lista = []
    # Agora eles começam bem mais longe
    zs = [0.05, 0.14, 0.24, 0.35, 0.47]
    lanes = [-0.45, 0, 0.45]

    usados = []

    for z in zs:
        lane = random.choice(lanes)

        # evita repetir a mesma faixa logo em sequência
        while len(usados) > 0 and lane == usados[-1]:
            lane = random.choice(lanes)

        usados.append(lane)

        lista.append({
            "z": z,
            "lane": lane,
            "tipo": random.choice(["bloco", "cone"])
        })

    return lista

obstaculos = criar_obstaculos_iniciais()

# ==============================
# FUNÇÕES
# ==============================
def desenhar_ceu():
    for y in range(horizonte_y):
        t = y / horizonte_y
        r = int(AZUL_TOPO[0] * (1 - t) + AZUL_BAIXO[0] * t)
        g = int(AZUL_TOPO[1] * (1 - t) + AZUL_BAIXO[1] * t)
        b = int(AZUL_TOPO[2] * (1 - t) + AZUL_BAIXO[2] * t)
        pygame.draw.line(tela, (r, g, b), (0, y), (LARGURA, y))

def desenhar_grama():
    pygame.draw.rect(tela, VERDE, (0, horizonte_y, LARGURA, ALTURA - horizonte_y))

def largura_pista(z):
    base = largura_base_topo
    fator = largura_base_baixo - largura_base_topo

    # profundidade mais forte
    zp = z ** 2.2
    return base + zp * fator

def centro_pista(z):
    # Até 100 pontos: pista reta
    # Depois de 100 pontos: continua reta (como você pediu)
    return centro_x

def desenhar_pista():
    for i in range(num_faixas):
        z1 = i / num_faixas
        z2 = (i + 1) / num_faixas

        p1 = z1 ** 1.7
        p2 = z2 ** 1.7

        y1 = horizonte_y + p1 * altura_util + scroll
        y2 = horizonte_y + p2 * altura_util + scroll

        if y1 >= ALTURA:
            y1 -= altura_util
        if y2 >= ALTURA:
            y2 -= altura_util

        if y2 < y1:
            y2 += altura_util

        w1 = largura_pista(z1)
        w2 = largura_pista(z2)

        c1 = centro_pista(z1)
        c2 = centro_pista(z2)

        x1e = c1 - w1 / 2
        x1d = c1 + w1 / 2
        x2e = c2 - w2 / 2
        x2d = c2 + w2 / 2

        cor = CINZA_1 if i % 2 == 0 else CINZA_2

        pygame.draw.polygon(tela, cor, [
            (x1e, y1),
            (x1d, y1),
            (x2d, y2),
            (x2e, y2)
        ])

        borda1 = max(3, w1 * 0.04)
        borda2 = max(3, w2 * 0.04)

        pygame.draw.polygon(tela, VERMELHO if i % 2 == 0 else BRANCO, [
            (x1e, y1),
            (x1e + borda1, y1),
            (x2e + borda2, y2),
            (x2e, y2)
        ])

        pygame.draw.polygon(tela, VERMELHO if i % 2 == 0 else BRANCO, [
            (x1d - borda1, y1),
            (x1d, y1),
            (x2d, y2),
            (x2d - borda2, y2)
        ])

        if i % 2 == 0:
            faixa1 = max(2, w1 * 0.015)
            faixa2 = max(2, w2 * 0.015)

            pygame.draw.polygon(tela, BRANCO, [
                (c1 - faixa1 / 2, y1),
                (c1 + faixa1 / 2, y1),
                (c2 + faixa2 / 2, y2),
                (c2 - faixa2 / 2, y2)
            ])

def desenhar_carro():
    pygame.draw.rect(tela, (20, 20, 20), (carro_x - 36, carro_y + 28, 72, 10))
    pygame.draw.rect(tela, VERMELHO, (carro_x - 40, carro_y - 2, 80, 32))
    pygame.draw.rect(tela, VERMELHO, (carro_x - 26, carro_y - 18, 52, 20))
    pygame.draw.rect(tela, (120, 30, 30), (carro_x - 16, carro_y - 12, 32, 10))
    pygame.draw.rect(tela, PRETO, (carro_x - 34, carro_y + 20, 12, 10))
    pygame.draw.rect(tela, PRETO, (carro_x + 22, carro_y + 20, 12, 10))
    pygame.draw.rect(tela, AMARELO, (carro_x - 30, carro_y + 8, 10, 8))
    pygame.draw.rect(tela, AMARELO, (carro_x + 20, carro_y + 8, 10, 8))

    # hitbox maior
    return pygame.Rect(carro_x - 38, carro_y - 14, 76, 46)

def desenhar_obstaculos(carro_rect):
    global game_over

    obstaculos_ordenados = sorted(obstaculos, key=lambda o: o["z"])

    for obs in obstaculos_ordenados:
        z = obs["z"]
        largura = largura_pista(z)
        centro = centro_pista(z)

        x = centro + obs["lane"] * largura * 0.42
        y = horizonte_y + z * altura_util

        larg = 26 + z * 52
        alt = 26 + z * 52

        if obs["tipo"] == "bloco":
            rect = pygame.Rect(int(x - larg / 2), int(y - alt / 2), int(larg), int(alt))
            pygame.draw.rect(tela, AMARELO, rect)
            pygame.draw.rect(tela, PRETO, rect, 2)
        else:
            topo = (x, y - alt / 2)
            esq = (x - larg / 2, y + alt / 2)
            dire = (x + larg / 2, y + alt / 2)
            pygame.draw.polygon(tela, LARANJA, [topo, esq, dire])
            rect = pygame.Rect(int(x - larg / 2), int(y - alt / 2), int(larg), int(alt))

        if rect.colliderect(carro_rect):
            game_over = True

def atualizar_obstaculos():
    global pontuacao

    # obstáculos "parados" na pista, mas a estrada anda;
    # quando passam do jogador, reaparecem no horizonte
    for obs in obstaculos:
        obs["z"] += 0.006

        if obs["z"] > 1.02:
            obs["z"] = random.uniform(0.03, 0.10)
            obs["lane"] = random.choice([-0.45, 0, 0.45])
            obs["tipo"] = random.choice(["bloco", "cone"])
            pontuacao += 10

def limites_pista_base():
    z = 1.0
    largura = largura_pista(z)
    centro = centro_pista(z)
    esquerda = centro - largura / 2
    direita = centro + largura / 2
    return esquerda, direita

def mostrar_hud():
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontos, (20, 20))

    if pontuacao < 100:
        fase = fonte_menor.render("Fase 1: reta com obstáculos", True, BRANCO)
    else:
        fase = fonte_menor.render("Fase 2: reta mantendo perspectiva e colisão", True, BRANCO)

    tela.blit(fase, (20, 55))

    if game_over:
        msg1 = fonte.render("GAME OVER", True, BRANCO)
        msg2 = fonte_menor.render("Aperte R para reiniciar", True, BRANCO)
        tela.blit(msg1, (LARGURA // 2 - msg1.get_width() // 2, 25))
        tela.blit(msg2, (LARGURA // 2 - msg2.get_width() // 2, 60))

def reiniciar():
    global carro_x, pontuacao, game_over, scroll, obstaculos

    carro_x = centro_x
    pontuacao = 0
    game_over = False
    scroll = 0
    obstaculos = criar_obstaculos_iniciais()

# ==============================
# LOOP PRINCIPAL
# ==============================
rodando = True
while rodando:
    dt = clock.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and game_over:
                reiniciar()

    teclas = pygame.key.get_pressed()

    if not game_over:
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            carro_x -= velocidade_carro
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            carro_x += velocidade_carro

        scroll += velocidade_scroll
        if scroll >= faixa_h:
            scroll = 0

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
sys.exit()