from PPlay.window import *
from PPlay.keyboard import *


def jogo1():
    janela = Window(1280,640)
    janela.set_title("Gabriel Salerno")

    teclado = Keyboard()

    while(True):
        janela.set_background_color([0,0,0])
        
        if teclado.key_pressed("ESCAPE"):
            break
        janela.update()