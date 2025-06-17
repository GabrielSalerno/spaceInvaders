from PPlay.window import *
from datetime import date

def criarRanking(nome,pontuacao):
    arquivo = open("ranking.txt","a")
    data= date.today()
    arquivo.write(f"{nome} {pontuacao} {data}")

def escreverRanking():
    arquivo = open("ranking.txt","r")
"""
def telaGameOver(janela,pontuacao):
    teclado = janela.get_keyboard()
    nome = ""
    while True:
        janela.set_background_color(0,0,0)
        janela.draw_text("Game Over", janela.width/2, janela.height/2, size=28, color=(142,50,0), font_name="Arial", bold=False, italic=False)
        janela.draw_text(nome,janela.width/2-30,janela.height/2-30, size=28, color=(142,50,0),font_name="Arial")
        janela.update()"""