from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.collision import *
from random import randint
from monstro import *
from nave import *
from arquivo import *

# Nome Gabriel Salerno
# Peguei o codigo do aluno Gabriel Nascimento Garcia

# Configuração da janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
window.set_title("Gabriel Nascimento Garcia")

# Dispositivos de entrada
mouse = window.get_mouse()
keyboard = window.get_keyboard()

# Estados do jogo
MENU = 0
JOGO = 1
DIFICULDADE = 2
RANKING = 3
estado_atual = MENU

# Carregar imagem de fundo
imagem_fundo = GameImage("sprites/bg.png") # GS - Alterei somente onde pega o arquivo
imagem_fundo.set_position(0, 0)

# GS - Carregar imagem nave
nave = criar_nave("sprites/nave.png",window)

# GS - Velocidade da nave
velnavex = 280

# GS - Velocidade do tiro
velTiroy = 200

# GS - Lista tiros
tiros = list()

# GS - Tiros monstros
tiros_monstros = list()

L = 4
C = 4
monstros = gerar_matriz(L,C,"sprites/monstro.png",40)
matrizVazia = False

velMonstrosx = 200
velMonstrosy = 20

# GS - Iniciando cronometro
tempo_ultimo_tiro = 0.5
recarga_tiro = 0.5
tempo_ultimo_tiro_monstro = 0.8
recarga_tiro_monstro = 0.8

# Propriedades dos botões
largura_botao = 300
altura_botao = 60
cor_botao_normal = (100, 100, 100)
cor_botao_hover = (150, 150, 150)
cor_texto_botao = (255, 255, 255)
cor_borda_botao = (255, 255, 255)
espacamento_botao = 30  # Espaço entre botões

# Calcular posições
posicao_titulo_y = 100
posicao_primeiro_botao_y = 250
posicoes_botoes = [
    posicao_primeiro_botao_y,
    posicao_primeiro_botao_y + altura_botao + espacamento_botao,
    posicao_primeiro_botao_y + (altura_botao + espacamento_botao) * 2,
    posicao_primeiro_botao_y + (altura_botao + espacamento_botao) * 3
]

# Posições e textos dos botões
botoes = [
    {"texto": "JOGAR", "x": WINDOW_WIDTH//2 - largura_botao//2, "y": posicoes_botoes[0]},
    {"texto": "DIFICULDADE", "x": WINDOW_WIDTH//2 - largura_botao//2, "y": posicoes_botoes[1]},
    {"texto": "RANKING", "x": WINDOW_WIDTH//2 - largura_botao//2, "y": posicoes_botoes[2]},
    {"texto": "SAIR", "x": WINDOW_WIDTH//2 - largura_botao//2, "y": posicoes_botoes[3]}
]

# Botões da tela de dificuldade
# Centralizados verticalmente na tela
INICIO_Y_BOTOES_DIF = 250
ESPACAMENTO_BOTOES_DIF = 30

botoes_dificuldade = [
    {"texto": "FÁCIL", "x": WINDOW_WIDTH//2 - largura_botao//2, "y": INICIO_Y_BOTOES_DIF},
    {"texto": "MÉDIO", "x": WINDOW_WIDTH//2 - largura_botao//2, "y": INICIO_Y_BOTOES_DIF + altura_botao + ESPACAMENTO_BOTOES_DIF},
    {"texto": "DIFÍCIL", "x": WINDOW_WIDTH//2 - largura_botao//2, "y": INICIO_Y_BOTOES_DIF + 2 * (altura_botao + ESPACAMENTO_BOTOES_DIF)}
]

def calcular_centro_texto(texto, tamanho_fonte):
    # Fator de ajuste para melhor centralização
    fator_ajuste = tamanho_fonte * 0.6  # Ajuste este valor conforme necessário
    return len(texto) * fator_ajuste

def mouse_sobre_botao(botao):
    mouse_x = mouse.get_position()[0]
    mouse_y = mouse.get_position()[1]
    return (botao["x"] <= mouse_x <= botao["x"] + largura_botao and 
            botao["y"] <= mouse_y <= botao["y"] + altura_botao)

def desenhar_botao(botao, esta_hover):
    # Calcular posição do texto para centralização perfeita
    largura_texto = calcular_centro_texto(botao["texto"], 32)
    texto_x = WINDOW_WIDTH//2 - largura_texto//2
    texto_y = botao["y"] + (altura_botao - 32) // 2
    
    # Desenhar texto do botão com cor diferente se estiver em hover
    cor = cor_botao_hover if esta_hover else cor_botao_normal
    window.draw_text(botao["texto"], texto_x, texto_y, size=32, color=cor)

def tratar_clique_botao(texto_botao):
    global estado_atual
    if texto_botao == "JOGAR":
        estado_atual = JOGO
    elif texto_botao == "DIFICULDADE":
        estado_atual = DIFICULDADE
    elif texto_botao == "RANKING":
        estado_atual = RANKING
    elif texto_botao == "SAIR":
        window.close()
        exit()

dif = 1 # GS - Adicionei a dificuldade padrão

def tratar_clique_dificuldade(texto_botao): # GS - Adicionei as dificuldades indo diretamente para o jogo e aumentando a dificuldade
    global estado_atual, dif
    if texto_botao == "FÁCIL":
        estado_atual = JOGO
        dif = 1
    elif texto_botao == "MÉDIO":
        estado_atual = JOGO
        dif = 2
    elif texto_botao == "DIFÍCIL":
        estado_atual = JOGO
        dif = 3

mouse_estava_pressionado = False  # Adicione isso antes do loop principal
direcao = 1
inverteu = False
gameover = False

vidas = 3
invencivel = False
tempo_invencivel = 0

contadorFrame = 0
tempoAcumuladoFPS = 0
fps = 0

pontuacao = 0

monstrosEmbaixo = []

rankingRegistrado = False

escudo100 = Sprite("sprites/escudo100.png",frames=1)
escudo100.x = (window.width-escudo100.width)/2
escudo100.y = window.height-115
escudo100.set_position(escudo100.x,escudo100.y)

escudo50 = Sprite("sprites/escudo50.png",frames=1)
escudo50.x = escudo100.x
escudo50.y = escudo100.y
escudo50.set_position(escudo50.x,escudo50.y)

primeira_vida_escudo = True
segunda_vida_escudo = False

while True:
    mouse_pressionado = mouse.is_button_pressed(1)

    # Estado do menu
    if estado_atual == MENU:
        # GS - Jogo ainda não iniciado para alterar a recarga do tiro de acordo com a dificuldade
        jogo_iniciado = False
        # Reiniciar todo o jogo

        imagem_fundo.draw()
        texto_titulo = "SPACE INVADERS"
        tamanho_fonte_titulo = 48
        largura_titulo = calcular_centro_texto(texto_titulo, tamanho_fonte_titulo)
        titulo_x = WINDOW_WIDTH//2 - largura_titulo//2
        window.draw_text(texto_titulo, titulo_x + 2, posicao_titulo_y + 2, size=tamanho_fonte_titulo, color=(50, 50, 50))
        window.draw_text(texto_titulo, titulo_x, posicao_titulo_y, size=tamanho_fonte_titulo, color=(255, 255, 255))
        for botao in botoes:
            esta_hover = mouse_sobre_botao(botao)
            desenhar_botao(botao, esta_hover)
            if esta_hover and mouse_pressionado and not mouse_estava_pressionado:
                tratar_clique_botao(botao["texto"])

    # Estado do jogo
    elif estado_atual == JOGO:
        
        # GS - Tempo entre tiros com dificuldade
        if not jogo_iniciado:
            recarga_tiro *= dif
            recarga_tiro_monstro /= dif
            jogo_iniciado = True 
        
        tempo_ultimo_tiro += window.delta_time()
        tempo_ultimo_tiro_monstro += window.delta_time()

        if not gameover:
            # GS - nave se mexendo com as setas e colidindo nas paredes
            mover(nave,velnavex,keyboard,window,dif)
            
            for l in monstros:
                for c in l:
                    c.x += velMonstrosx * direcao * window.delta_time()

            if monstros and monstros[0]:
                monstroEsquerda = monstros[0][0]
                monstroDireita = monstros[0][-1]

            if not inverteu:                   
                if monstroDireita.width + monstroDireita.x >= window.width or monstroEsquerda.x <= 0:
                    direcao *= -1
                    for l in monstros:     
                        for c in l:
                            c.y += velMonstrosy
                    inverteu = True
            
            if inverteu:
                if monstroEsquerda.x > 0 and monstroDireita.width + monstroDireita.x < window.width:
                    inverteu = False
            
            monstrosEmbaixo = []
            for linha in monstros:
                if linha:
                    monstrosEmbaixo.append(linha[-1])

            for l in monstrosEmbaixo:
                if (l.y + l.height >= nave.y):
                    gameover = True

            if tempo_ultimo_tiro_monstro >= recarga_tiro_monstro:
                linhas_disponiveis = [linha for linha in monstros if len(linha) > 0]
                if linhas_disponiveis:
                    linha_aleatoria = linhas_disponiveis[randint(0, len(linhas_disponiveis)-1)]
                    atirador = linha_aleatoria[randint(0, len(linha_aleatoria)-1)]
                    tiro_monstro = Sprite("sprites/tiroMonstro.png")
                    tiro_monstro.x = atirador.x + (atirador.width/2)
                    tiro_monstro.y = atirador.y + atirador.height
                    tiros_monstros.append(tiro_monstro)
                    tempo_ultimo_tiro_monstro = 0
            
            if len(tiros_monstros) > 0:
                for i in tiros_monstros:
                    i.y = i.y + velTiroy * window.delta_time()
            
            for tiro_monstro in tiros_monstros:
                if tiro_monstro.collided(nave) and not invencivel:
                    vidas -= 1
                    nave.x = (window.width-nave.width)/2
                    nave.y = window.height-nave.height
                    nave.set_position(nave.x,nave.y)
                    invencivel = True
                    tiros_monstros.remove(tiro_monstro)
                elif tiro_monstro.y > window.height:
                    tiros_monstros.remove(tiro_monstro)
            
            if tempo_invencivel >= 2:
                invencivel = False

            if keyboard.key_pressed("space") and tempo_ultimo_tiro >= recarga_tiro:
                tiro = Sprite("sprites/tiro.png",frames=1)
                tiro.x = nave.x + (nave.width/2)
                tiro.y = nave.y
                tiros.append(tiro)
                tempo_ultimo_tiro = 0

            if len(tiros) > 0:
                for i in tiros:
                    i.y = i.y + velTiroy * window.delta_time() * -1
            
            for c in range(len(tiros)-1,-1,-1):
                    if tiros[c].y + tiros[c].height < 0:
                        del tiros[c]
            
            for t in range(len(tiros)-1,-1,-1):
                tiro = tiros[t]
                for monstro in monstrosEmbaixo:
                    if (monstroEsquerda.x <= tiro.x+tiro.width and tiro.x <= monstroDireita.x+monstroDireita.width) and (tiro.y <= monstro.y+monstro.height):
                        colisao_ocorreu = False
                        for l in monstros:
                            for monstro in l:
                                if monstro and tiro.collided(monstro):
                                    pontuacao += 1
                                    l.remove(monstro)
                                    if len(l)==0:
                                        monstros.remove(l)
                                    monstrosEmbaixo = []
                                    for linha in monstros:
                                        if linha:
                                            monstrosEmbaixo.append(linha[-1])
                                    tiros.pop(t)
                                    colisao_ocorreu = True
                                    break
                                if colisao_ocorreu:
                                    break
        
        todasLinhasvazias = all(len(linha)==0 for linha in monstros)
        if todasLinhasvazias:
            L = 4
            C = 4
            monstros = gerar_matriz(L,C,"sprites/monstro.png",40)
            velMonstrosx += 100
            velMonstrosy += 20
            tempo_ultimo_tiro_monstro -= 0.1
            recarga_tiro_monstro -= 0.1
            direção = 1
            inverteu = False
        

        tempoAcumuladoFPS += window.delta_time()
        contadorFrame += 1

        if tempoAcumuladoFPS >= 1:
            fps = contadorFrame
            contadorFrame = 0
            tempoAcumuladoFPS = 0

        if primeira_vida_escudo or segunda_vida_escudo:
            for c in range(len(tiros)-1,-1,-1):
                if tiros[c].collided(escudo100):
                    del tiros[c]
                elif tiros[c].collided(escudo50):
                    del tiros[c]
        
        if primeira_vida_escudo:
            for c in range(len(tiros_monstros)-1,-1,-1):
                if tiros_monstros[c].collided(escudo100):
                    del tiros_monstros[c]
                    if primeira_vida_escudo:
                        primeira_vida_escudo = False
                        segunda_vida_escudo = True
        elif segunda_vida_escudo:
            for c in range(len(tiros_monstros)-1,-1,-1):
                    if tiros_monstros[c].collided(escudo50):
                        del tiros_monstros[c]
                        segunda_vida_escudo = False

        imagem_fundo.draw()

        if primeira_vida_escudo:
            escudo100.draw()
        if segunda_vida_escudo:
            escudo50.draw()

        window.draw_text(str(fps), window.width-58,10, size=32, color=(255, 255, 255),font_name="Arial")

        for i in tiros:
            i.draw()
        for l in monstros:
            for c in l:
                c.draw()
        for tirosMonstro in tiros_monstros:
            tirosMonstro.draw()
        
        if invencivel:
            tempo_invencivel += window.delta_time()
            if int(tempo_invencivel*8)%2==0:
                nave.draw()
            if tempo_invencivel >2:
                invencivel = False
                tempo_invencivel = 0
        else:
            if not gameover:
                nave.draw()

        if gameover or vidas == 0:
            gameover = True
            window.draw_text("Game Over", window.width/2, window.height/2, size=28, color=(142,50,0), font_name="Arial")
            if not rankingRegistrado:
                nome = input("Nome: ")
                criarRanking(nome,pontuacao)
                rankingRegistrado = True
            jogo_iniciado = False

        window.draw_text(f"Vidas: {vidas}",8,10,size=28,color=(255,255,255),font_name="Arial")

        # GS - Apaguei o texto que tinha, para avisando q apertar esc saia do jogo
        if keyboard.key_pressed("ESC"):
            estado_atual = MENU

    # Estado de dificuldade
    elif estado_atual == DIFICULDADE:
        imagem_fundo.draw()
        titulo_dif = "SELECIONE A DIFICULDADE"
        tamanho_fonte_titulo_dif = 40
        largura_titulo_dif = calcular_centro_texto(titulo_dif, tamanho_fonte_titulo_dif)
        titulo_dif_x = WINDOW_WIDTH//2 - largura_titulo_dif//2
        titulo_dif_y = 150
        window.draw_text(titulo_dif, titulo_dif_x + 2, titulo_dif_y + 2, size=tamanho_fonte_titulo_dif, color=(50, 50, 50))
        window.draw_text(titulo_dif, titulo_dif_x, titulo_dif_y, size=tamanho_fonte_titulo_dif, color=(255, 255, 255))
        for botao in botoes_dificuldade:
            esta_hover = mouse_sobre_botao(botao)
            desenhar_botao(botao, esta_hover)
            if esta_hover and mouse_pressionado and not mouse_estava_pressionado:
                tratar_clique_dificuldade(botao["texto"])
        if keyboard.key_pressed("ESC"):
            estado_atual = MENU

    # Estado de ranking
    elif estado_atual == RANKING:
        imagem_fundo.draw()
        window.draw_text("TOP 5 RANKING", window.width//2 - 150, 50, size=40, color=(255, 255, 255))
        ranking = lerRanking()
        y = 150
        for i, (nome, pontuacao, data) in enumerate(ranking):
            texto = f"{i+1}. {nome} - {pontuacao} pts - {data}"
            window.draw_text(texto, 100, y, size=30, color=(255, 255, 255))
            y += 50
        if keyboard.key_pressed("ESC"):
            estado_atual = MENU

    mouse_estava_pressionado = mouse_pressionado  # Atualize o estado do mouse

    window.update()