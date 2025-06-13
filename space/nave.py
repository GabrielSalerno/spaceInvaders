from PPlay.sprite import Sprite

def criar_nave(imagem,window,):
    nave = Sprite(imagem,frames=1)
    nave.x = (window.width-nave.width)/2
    nave.y = window.height-nave.height
    nave.set_position(nave.x,nave.y)
    return nave

def mover(self, teclado, window, dificuldade):
    if teclado.key_pressed("right") and self.nave.x + self.nave.width <= window.width:
        self.nave.x += self.velocidade * window.delta_time() / dificuldade
    if teclado.key_pressed("left") and self.nave.x >= 0:
        self.nave.x -= self.velocidade * window.delta_time() / dificuldade

def desenhar(self):
    self.nave.draw()
