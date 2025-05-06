from PPlay.window import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.keyboard import *

janela = Window(1280,640)
janela.set_title("Gabriel Salerno")

mou = Mouse()
teclado = Keyboard()

jogo_iniciado = False
dificuldade_select = False

botaoJogar = Sprite("spaceInvaders/objetos/botaoJogar.png", frames=1)
botaoJogar.x = (janela.width - botaoJogar.width)/2
botaoJogar.y = (botaoJogar.height)
botaoJogar.set_position(botaoJogar.x,botaoJogar.y)

botaoDif = Sprite("spaceInvaders/objetos/botaoDif.png", frames=1)
botaoDif.x = (janela.width - botaoDif.width)/2
botaoDif.y = (botaoDif.height + 100)
botaoDif.set_position(botaoDif.x,botaoDif.y)

botaoRank = Sprite("spaceInvaders/objetos/botaoRank.png", frames=1)
botaoRank.x = (janela.width - botaoRank.width)/2
botaoRank.y = (botaoRank.height + 200)
botaoRank.set_position(botaoRank.x,botaoRank.y)

botaoSair = Sprite("spaceInvaders/objetos/botaoSair.png", frames=1)
botaoSair.x = (janela.width - botaoSair.width)/2
botaoSair.y = (botaoSair.height + 300)
botaoSair.set_position(botaoSair.x,botaoSair.y)

# Botões da janela de dificuldade
botaoFacil = Sprite("spaceInvaders/objetos/botaoFacil.png",frames=1)
botaoFacil.x = (janela.width - botaoFacil.width)/2
botaoFacil.y = (botaoFacil.height+150)
botaoFacil.set_position(botaoFacil.x,botaoFacil.y)

botaoMed = Sprite("spaceInvaders/objetos/botaoMed.png", frames=1)
botaoMed.x = (janela.width - botaoMed.width)/2
botaoMed.y = (janela.height - botaoMed.height)/2
botaoMed.set_position(botaoMed.x,botaoMed.y)

botaoDificil = Sprite("spaceInvaders/objetos/botaoDificil.png", frames=1)
botaoDificil.x = (janela.width - botaoDificil.width)/2
botaoDificil.y = ((janela.height - botaoMed.height)/2) + 85
botaoDificil.set_position(botaoDificil.x,botaoDificil.y)

dificulade = 1

while(True):
    # Tela do jogo
    if jogo_iniciado == True:
        janela.set_background_color([0,0,0])
        
        if teclado.key_pressed("ESCAPE"):
            jogo_iniciado = False
        
        janela.update()

    # Tela da Dificuldade
    if dificuldade_select == True:
        janela.set_background_color([100,125,25])

        if (mou.is_over_area([botaoFacil.x,botaoFacil.y],[botaoFacil.x+botaoFacil.width,botaoFacil.y+botaoFacil.height]) and (mou.is_button_pressed(1))):
            dificulade = 1
            jogo_iniciado = True
            dificuldade_select = False

        if (mou.is_over_area([botaoMed.x,botaoMed.y],[botaoMed.x+botaoMed.width,botaoMed.y+botaoMed.height]) and (mou.is_button_pressed(1))):
            dificulade = 2
            jogo_iniciado = True
            dificuldade_select = False
        
        if (mou.is_over_area([botaoDificil.x,botaoDificil.y],[botaoDificil.x+botaoDificil.width,botaoDificil.y+botaoDificil.height]) and (mou.is_button_pressed(1))):
            dificulade = 3
            jogo_iniciado = True
            dificuldade_select = False

        botaoFacil.draw()
        botaoMed.draw()
        botaoDificil.draw()
        janela.update()

    # Tela do Menu
    janela.set_background_color([100,125,25])

    if (mou.is_over_area([botaoJogar.x,botaoJogar.y],[botaoJogar.x+botaoJogar.width,botaoJogar.y+botaoJogar.height]) and (mou.is_button_pressed(1))):
        jogo_iniciado = True

    if (mou.is_over_area([botaoDif.x,botaoDif.y],[botaoDif.x+botaoDif.width,botaoDif.y+botaoDif.height]) and (mou.is_button_pressed(1))):
        dificuldade_select = True

    if (mou.is_over_area([botaoSair.x,botaoSair.y],[botaoSair.x+botaoSair.width,botaoSair.y+botaoSair.height]) and (mou.is_button_pressed(1))):
        janela.close()

    if jogo_iniciado == False and dificuldade_select == False:
        botaoJogar.draw()
        botaoDif.draw()
        botaoRank.draw()
        botaoSair.draw()
        janela.update()

# dificulade = 1 (facil)(padrão) ou 2 (media) ou 3 (dificil)
