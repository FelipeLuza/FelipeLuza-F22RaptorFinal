from Recursos.funcoes2 import mensagem_inicio, ouvir_comando, falar_frase_inicial
import pygame
import random
import json

pygame.init()


# Tela e configurações iniciais
tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("F-22 Raptor: Zona de Combate")
relogio = pygame.time.Clock()

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Recursos
caca = pygame.transform.scale(pygame.image.load("Recursos/cacaF22.png"), (300, 100))
cacaInimigo = pygame.transform.scale(pygame.image.load("Recursos/cacaF22.png"), (300, 100))
fundoStart = pygame.image.load("Recursos/fundoStart.jpg")
fundoJogo = pygame.transform.scale(pygame.image.load("Recursos/fundoBatalha.jpeg"), tamanho)
missil = pygame.image.load("Recursos/missil.png")
img_explosao = pygame.image.load("Recursos/explosao.png").convert_alpha()
missileSound = pygame.mixer.Sound("Recursos/missil.wav")
explosaoSound = pygame.mixer.Sound("Recursos/explosao.wav")
som_comunicacao = pygame.mixer.Sound("Recursos/comunicacao.wav")
iron = pygame.image.load("Recursos/iron.png")

# Fontes
fonteMenu = pygame.font.SysFont("comicsans", 24)
fonteMorte = pygame.font.SysFont("arial", 32)
fontePause = pygame.font.SysFont("arial", 72)

def escreverDados(nome, pontos):
    from datetime import datetime

    try:
        with open("log.dat", "r") as f:
            dados = json.load(f)
    except:
        dados = {}

    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")

    dados[nome] = {
        "pontos": pontos,
        "data": data,
        "hora": hora
    }

    with open("log.dat", "w") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def lerUltimosRegistros(n=5):
    try:
        with open("log.dat", "r") as f:
            dados = json.load(f)
    except:
        return []

    registros_validos = []

    for nome, info in dados.items():
        if isinstance(info, dict) and all(k in info for k in ["pontos", "data", "hora"]):
            registros_validos.append((nome, info))

    return registros_validos[-n:]


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

def tela_boas_vindas(nome):
    esperando_tecla = True
    som_comunicacao.stop()  
    falar_frase_inicial(nome)

    while esperando_tecla:
        tela.fill(preto)
        titulo = fonteMorte.render(f"Bem-vindo, {nome}!", True, branco)
        explicacao1 = fonteMenu.render("Você controla o caça abaixo.", True, branco)
        explicacao2 = fonteMenu.render("Desvie dos mísseis do inimigo e marque pontos!", True, branco)
        tecla_msg = fonteMenu.render("Pressione ESPAÇO ou TAB e fale 'jogar' para começar", True, branco)

        tela.blit(titulo, (300, 150))
        tela.blit(explicacao1, (280, 220))
        tela.blit(explicacao2, (200, 260))
        tela.blit(tecla_msg, (250, 400))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    som_comunicacao.stop()
                    esperando_tecla = False
                elif evento.key == pygame.K_TAB:
                    som_comunicacao.stop()
                    print("Ouvindo... fale 'jogar'")
                    if ouvir_comando():
                        print("Comando de voz aceito!")
                        som_comunicacao.stop()
                        esperando_tecla = False

def jogar():
    pontos = 0
    nome = digitar_nome()
    tela_boas_vindas(nome)

    posicaoX_caca = (1000 - caca.get_width()) // 2
    posicaoY_caca = 700 - caca.get_height() - 10
    movimentoX_caca = 0
    movimentoY_caca = 0

    posicaoXInimigo = 400
    posicaoYInimigo = 0
    velocidadeInimigo = 8
    direcaoInimigo = 1

    velocidadeMissel = 5
    velocidade_maxima = 20
    ultimo_aumento = pygame.time.get_ticks()

    posicoesMisseis = []
    canais_misseis = []
    larguraCaca = caca.get_width()
    alturaCaca = caca.get_height()
    larguraMissil = missil.get_width()
    alturaMissil = missil.get_height()

    iron_img = pygame.transform.scale(pygame.image.load("Recursos/iron.png"), (50, 50))
    iron_x = random.randint(100, 800)
    iron_y = random.randint(80, 120)
    iron_dx = random.uniform(-1.2, 1.2)
    iron_dy = random.uniform(-0.5, 0.5)

    tempo_disparo = 0
    tempo_entre_disparos = 900

    raio_sol = 40              
    raio_min = 35              
    raio_max = 45             
    raio_direcao = 0.05         

    pausado = False
    velocidade_caca = 25

    while True:
        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                if not pausado:
                    if evento.key == pygame.K_RIGHT:
                        movimentoX_caca = velocidade_caca
                        movimentoY_caca = 0
                    elif evento.key == pygame.K_LEFT:
                        movimentoX_caca = -velocidade_caca
                        movimentoY_caca = 0
                    elif evento.key == pygame.K_UP:
                        movimentoY_caca = -velocidade_caca
                        movimentoX_caca = 0
                    elif evento.key == pygame.K_DOWN:
                        movimentoY_caca = velocidade_caca
                        movimentoX_caca = 0
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoX_caca = 0
                if evento.key in [pygame.K_UP, pygame.K_DOWN]:
                    movimentoY_caca = 0

        if pausado:
            texto_pause = fontePause.render("PAUSE", True, branco)
            tela.blit(texto_pause, (tamanho[0] // 2 - 100, tamanho[1] // 2 - 50))
            pygame.display.update()
            relogio.tick(15)
            continue

        posicaoX_caca += movimentoX_caca
        posicaoY_caca += movimentoY_caca
        posicaoX_caca = max(0, min(posicaoX_caca, 1000 - larguraCaca))
        posicaoY_caca = max(0, min(posicaoY_caca, 600))

        posicaoXInimigo += velocidadeInimigo * direcaoInimigo
        if posicaoXInimigo <= 0 or posicaoXInimigo >= 1000 - cacaInimigo.get_width():
            direcaoInimigo *= -1

        if len(posicoesMisseis) == 0 and tempo_atual - tempo_disparo >= tempo_entre_disparos:
            missilX = posicaoXInimigo + (cacaInimigo.get_width() // 2) - (missil.get_width() // 2)
            missilY = posicaoYInimigo + cacaInimigo.get_height()
            posicoesMisseis.append([missilX, missilY])
            novo_canal = pygame.mixer.find_channel()
            if novo_canal:
                novo_canal.set_volume(1.0)
                novo_canal.play(missileSound)
                canais_misseis.append(novo_canal)
            tempo_disparo = tempo_atual
            if tempo_entre_disparos > 300:
                tempo_entre_disparos -= 20

        canais_misseis = [c for c in canais_misseis if c.get_busy()]

        if tempo_atual - ultimo_aumento > 5000 and velocidadeMissel < velocidade_maxima:
            velocidadeMissel += 1
            ultimo_aumento = tempo_atual

        tela.blit(fundoJogo, (0, 0))
        tela.blit(cacaInimigo, (posicaoXInimigo, posicaoYInimigo))
        tela.blit(caca, (posicaoX_caca, posicaoY_caca))

        for missil_pos in posicoesMisseis[:]:
            missil_pos[1] += velocidadeMissel
            tela.blit(missil, (missil_pos[0], missil_pos[1]))

            colX = range(posicaoX_caca, posicaoX_caca + larguraCaca)
            colY = range(posicaoY_caca, posicaoY_caca + alturaCaca)
            colMX = range(missil_pos[0], missil_pos[0] + larguraMissil)
            colMY = range(missil_pos[1], missil_pos[1] + alturaMissil)

            if set(colX).intersection(colMX) and set(colY).intersection(colMY):
                escreverDados(nome, pontos)
                pygame.mixer.stop()
                pygame.mixer.Sound.play(explosaoSound)
                tela.blit(fundoJogo, (0, 0))
                explosao_x = (1000 - img_explosao.get_width()) // 2
                explosao_y = (700 - img_explosao.get_height()) // 2
                tela.blit(img_explosao, (explosao_x, explosao_y))
                texto_gameover = fonteMorte.render(f"Game Over! Pontos: {pontos}", True, branco)
                tela.blit(texto_gameover, (200, 100))
                registros = lerUltimosRegistros()
                fonte_registro = pygame.font.SysFont("arial", 20)
                y_base = 160
                for i, (nome_r, info) in enumerate(registros):
                    texto = f"{nome_r} - {info['pontos']} pts - {info['data']} {info['hora']}"
                    linha = fonte_registro.render(texto, True, branco)
                    tela.blit(linha, (200, y_base + i * 30))
                pygame.display.update()
                pygame.time.wait(5000)
                return

            if missil_pos[1] > 700:
                posicoesMisseis.remove(missil_pos)
                pontos += 1

        # ✅ Verificação da vitória (fora do for)
        if pontos >= 50:
            escreverDados(nome, pontos)
            pygame.mixer.stop()
            tela.blit(fundoJogo, (0, 0))
            texto_vitoria = fonteMorte.render(f"Missão cumprida, piloto! Pontuação final: {pontos}", True, branco)
            tela.blit(texto_vitoria, (180, 200))
            texto_instrucao = fonteMenu.render("Você salvou o mundo! Pressione qualquer tecla para encerrar a missão.", True, branco)
            tela.blit(texto_instrucao, (120, 300))
            pygame.display.update()
            pygame.event.clear()
            esperando_saida = True
            while esperando_saida:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        quit()
                    elif evento.type == pygame.KEYDOWN:
                        esperando_saida = False

            return

        texto_pontos = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto_pontos, (10, 10))
        texto_pausa = fonteMenu.render("Press Space to Pause Game", True, (200, 200, 200))
        tela.blit(texto_pausa, (180, 10))

        colX_inimigo = range(posicaoXInimigo, posicaoXInimigo + cacaInimigo.get_width())
        colY_inimigo = range(posicaoYInimigo, posicaoYInimigo + cacaInimigo.get_height())

        if set(colX).intersection(colX_inimigo) and set(colY).intersection(colY_inimigo):
            escreverDados(nome, pontos)
            pygame.mixer.stop()
            pygame.mixer.Sound.play(explosaoSound)
            tela.blit(fundoJogo, (0, 0))
            tela.blit(img_explosao, (posicaoX_caca, posicaoY_caca))
            texto_gameover = fonteMorte.render(f"Colidiu com o inimigo! Pontos: {pontos}", True, branco)
            tela.blit(texto_gameover, (200, 300))
            pygame.display.update()
            pygame.time.wait(3000)
            return

        # Objetos decorativos
        iron_x += iron_dx
        iron_y += iron_dy
        if iron_x <= 0 or iron_x >= 900:
            iron_dx *= -1
            iron_dx += random.uniform(-0.3, 0.3)
        if iron_y <= 80 or iron_y >= 130:
            iron_dy *= -1
            iron_dy += random.uniform(-0.2, 0.2)
        tela.blit(iron_img, (int(iron_x), int(iron_y)))

        # Sol pulsante
        raio_sol += raio_direcao
        if raio_sol >= raio_max or raio_sol <= raio_min:
            raio_direcao *= -1
        pygame.draw.circle(tela, (255, 255, 0), (950, 50), int(raio_sol))

        pygame.display.update()
        relogio.tick(60)


def menu():
    som_tocado = False

    while True:
        if not som_tocado:
            pygame.mixer.stop()
            som_comunicacao.play()
            som_tocado = True

        tela.blit(fundoStart, (0, 0))
        start = fonteMenu.render("Pressione ENTER para Jogar", True, preto)
        tela.blit(start, (290, 300))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    som_tocado = False
                    jogar()

menu()
