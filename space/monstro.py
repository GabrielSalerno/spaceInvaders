from PPlay.sprite import *

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