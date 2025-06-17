from PPlay.sprite import Sprite

def criar_nave(imagem,window):
    nave = Sprite(imagem,frames=1)
    nave.x = (window.width-nave.width)/2
    nave.y = window.height-nave.height
    nave.set_position(nave.x,nave.y)
    return nave

def mover(nave, velocidade,teclado, window, dificuldade):
    if teclado.key_pressed("right") and nave.x + nave.width <= window.width:
        nave.x += velocidade * window.delta_time() / dificuldade
    if teclado.key_pressed("left") and nave.x >= 0:
        nave.x -= velocidade * window.delta_time() / dificuldade

