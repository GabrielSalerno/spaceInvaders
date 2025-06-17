from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.collision import *
from random import randint

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