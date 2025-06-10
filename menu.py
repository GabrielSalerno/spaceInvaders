from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.collision import *
from random import randint

#Peguei o codigo do aluno Gabriel Nascimento Garcia

# tiro mata o player e tem que ir para o centro da tela, pisca por 2 segundo e fica imortal nesse tempo, contador de vidas na
# tela (começa com 3 vidas), quando zerar game over

def gerar_matriz(l,c,arquivo_sprite):
    monstros = list()

    for lin in range(l):
        linha = list()
        for col in range(c):
            monstro = Sprite(arquivo_sprite,frames=1)
            monstro.x = col * ((monstro.width/2) + monstro.width)
            monstro.y = lin * ((monstro.height/2) + monstro.height) + 40
            monstro.set_position(monstro.x,monstro.y)
            linha.append(monstro)
        monstros.append(linha)
    return monstros

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
imagem_fundo = GameImage("bg.png") # GS - Alterei somente onde pega o arquivo
imagem_fundo.set_position(0, 0)

# GS - Carregar imagem nave
nave = Sprite("nave.png",frames=1)
nave.x = (window.width-nave.width)/2
nave.y = window.height-nave.height
nave.set_position(nave.x,nave.y)

# GS - Velocidade da nave
velNavex = 280

# GS - Velocidade do tiro
velTiroy = 200

# GS - Lista tiros
tiros = list()

# GS - Tiros monstros
tiros_monstros = list()

L = 4
C = 4
monstros = gerar_matriz(L,C,"monstro.png")

velMonstrosx = 250
velMonstrosy = 30

# GS - Iniciando cronometro
tempo_ultimo_tiro = 0.2
tempo_ultimo_tiro_monstro = 0.2
recarga_tiro = 0.2
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

while True:
    mouse_pressionado = mouse.is_button_pressed(1)

    # Estado do menu
    if estado_atual == MENU:
        # GS - Jogo ainda não iniciado para alterar a recarga do tiro de acordo com a dificuldade
        jogo_iniciado = False
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
            # GS - Nave se mexendo com as setas e colidindo nas paredes
            if nave.x + nave.width <= window.width:
                if keyboard.key_pressed("right"):
                    nave.x = nave.x + velNavex * window.delta_time() / dif
            if nave.x >= 0:
                if keyboard.key_pressed("left"):
                    nave.x = nave.x + velNavex * window.delta_time() * -1 / dif

            for l in monstros:
                for c in l:
                    c.x += velMonstrosx * direcao * window.delta_time()

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
            
            monstrosEmbaixo = monstros[-1]

            for l in monstrosEmbaixo:
                if (l.y + l.height >= nave.y):
                    gameover = True

        if tempo_ultimo_tiro_monstro >= recarga_tiro_monstro:
            atirador = monstros[randint(0,len(monstros[0])-1)][randint(0,len(monstros)-1)]#mudei
            tiro_monstro = Sprite("tiroMonstro.png")
            tiro_monstro.x = atirador.x + (atirador.width/2)
            tiro_monstro.y = atirador.y + atirador.height
            tiros_monstros.append(tiro_monstro)
            tempo_ultimo_tiro_monstro = 0
        
        if len(tiros_monstros) > 0:
            for i in tiros_monstros:
                i.y = i.y + velTiroy * window.delta_time()
        
        for tiro in tiros_monstros: #mudei
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
            tiro = Sprite("tiro.png",frames=1)
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
        
        for t in range(len(tiros)):
            tiro = tiros[t]
            if (monstroEsquerda.x <= tiro.x+tiro.width and tiro.x <= monstroDireita.x+monstroDireita.width) and (tiro.y <= monstrosEmbaixo[0].y+monstrosEmbaixo[0].height):
                    for l in monstros:
                        for monstro in l:
                            if monstro and tiro.collided(monstro):
                                l.remove(monstro)
                                tiros.remove(tiro)
                                break
        
        tempoAcumuladoFPS += window.delta_time()
        contadorFrame += 1

        if tempoAcumuladoFPS >= 1:
            fps = contadorFrame
            contadorFrame = 0

        window.draw_text(str(fps), window.width/2,window.height/2, size=32, color=(255, 255, 255),font_name="Arial")

        imagem_fundo.draw()
        nave.draw()
        for i in tiros:
            i.draw()
        for l in monstros:
            for c in l:
                c.draw()
        for tirosMonstro in tiros_monstros:
            tirosMonstro.draw()
        
        if invencivel:
            tempo_invencivel += window.delta_time()


        if gameover or vidas == 0:
            window.draw_text("Game Over", window.width/2, window.height/2, size=28, color=(142,50,0), font_name="Arial", bold=False, italic=False)
        window.draw_text(f"Vidas: {vidas}",20,20,size=28,color=(255,255,255),font_name="Arial")

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
        texto_ranking = "Tela de Ranking - Pressione ESC para voltar"
        largura_texto_ranking = calcular_centro_texto(texto_ranking, 32)
        texto_ranking_x = WINDOW_WIDTH//2 - largura_texto_ranking//2
        window.draw_text(texto_ranking, texto_ranking_x, WINDOW_HEIGHT//2, size=32, color=(255, 255, 255))
        if keyboard.key_pressed("ESC"):
            estado_atual = MENU

    mouse_estava_pressionado = mouse_pressionado  # Atualize o estado do mouse

    window.update()