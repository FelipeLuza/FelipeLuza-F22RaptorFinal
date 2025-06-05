from Recursos.funcoes2 import mensagem_inicio
import pygame
import random
import json
import os

pygame.init()

# Inicializa o banco (fake)
def escreverDados(nome, pontos):
    try:
        with open("base.atitus", "r") as f:
            dados = json.load(f)
    except:
        dados = {}
    from datetime import datetime
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    dados[nome] = [pontos, agora]
    with open("base.atitus", "w") as f:
        json.dump(dados, f)

tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Iron Man: Projeto Final")
relogio = pygame.time.Clock()

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Carregar imagens e sons
iron = pygame.image.load("Recursos/iron.png")
fundoJogo = pygame.transform.scale(
    pygame.image.load("Recursos/fundoBatalha.jpg"), (1000, 700)
)
fundoDead = pygame.image.load("Recursos/fundoDead.png")
missel = pygame.image.load("Recursos/missile.png")
missileSound = pygame.mixer.Sound("Recursos/missile.wav")
explosaoSound = pygame.mixer.Sound("Recursos/explosao.wav")
pygame.mixer.music.load("Recursos/ironsound.mp3")

fonteMenu = pygame.font.SysFont("comicsans", 24)
fonteMorte = pygame.font.SysFont("arial", 32)

# Tela inicial para digitar o nome com pygame
def digitar_nome():
    nome = ""
    digitando = True
    while digitando:
        tela.fill(preto)
        texto = fonteMenu.render("Digite seu nome e pressione Enter:", True, branco)
        tela.blit(texto, (200, 200))
        nome_render = fonteMenu.render(nome, True, branco)
        tela.blit(nome_render, (200, 240))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome:
                    return nome
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 12:
                        nome += evento.unicode

# Função principal do jogo
def jogar():
    nome = digitar_nome()
    mensagem = mensagem_inicio(nome)
    tela.fill(preto)
    texto_msg = fonteMenu.render(mensagem, True, branco)
    tela.blit(texto_msg, (100, 300))
    pygame.display.update()
    pygame.time.wait(2000)  # espera 2 segundos

    

    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False



    posicaoX = 400
    posicaoY = 300
    movimentoX = 0
    movimentoY = 0
    velocidadeMissel = 1
    posicaoXMissel = random.randint(0, 750)
    posicaoYMissel = -240
    pontos = 0

    larguraIron = 250
    alturaIron = 127
    larguraMissel = 50
    alturaMissel = 250

    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoX = 10
                elif evento.key == pygame.K_LEFT:
                    movimentoX = -10
                elif evento.key == pygame.K_UP:
                    movimentoY = -10
                elif evento.key == pygame.K_DOWN:
                    movimentoY = 10
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoX = 0
                if evento.key in [pygame.K_UP, pygame.K_DOWN]:
                    movimentoY = 0

        posicaoX += movimentoX
        posicaoY += movimentoY

        # Limites
        posicaoX = max(0, min(posicaoX, 550))
        posicaoY = max(0, min(posicaoY, 473))

        tela.blit(fundoJogo, (0, 0))
        tela.blit(iron, (posicaoX, posicaoY))

        posicaoYMissel += velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos += 1
            velocidadeMissel += 1
            posicaoXMissel = random.randint(0, 750)
            pygame.mixer.Sound.play(missileSound)

        tela.blit(missel, (posicaoXMissel, posicaoYMissel))

        texto_pontos = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto_pontos, (10, 10))

        colX = range(posicaoX, posicaoX + larguraIron)
        colY = range(posicaoY, posicaoY + alturaIron)
        colMX = range(posicaoXMissel, posicaoXMissel + larguraMissel)
        colMY = range(posicaoYMissel, posicaoYMissel + alturaMissel)

        if set(colX).intersection(colMX) and set(colY).intersection(colMY):
            escreverDados(nome, pontos)
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(explosaoSound)
            tela.blit(fundoDead, (0, 0))
            texto_gameover = fonteMorte.render(f"Game Over! Pontos: {pontos}", True, branco)
            tela.blit(texto_gameover, (200, 300))
            pygame.display.update()
            pygame.time.wait(3000)
            return

        pygame.display.update()
        relogio.tick(60)


# Menu inicial
def menu():
    while True:
        tela.blit(fundoJogo, (0, 0))
        titulo = fonteMorte.render("Iron Man do Marcão", True, branco)
        tela.blit(titulo, (200, 200))
        start = fonteMenu.render("Pressione ENTER para Jogar", True, branco)
        tela.blit(start, (240, 300))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    jogar()


menu()
