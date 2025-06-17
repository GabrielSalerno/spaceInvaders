from PPlay.window import *
from datetime import date

def criarRanking(nome,pontuacao):
    with open("ranking.txt","a") as arquivo:
        data= date.today()
        arquivo.write(f"{nome} {pontuacao} {data}\n")

def lerRanking():
    try:
        with open("ranking.txt", "r") as arquivo:
            linhas = arquivo.readlines()
        ranking = []
        for linha in linhas:
            partes = linha.strip().split()
            if len(partes) >= 3:
                nome = " ".join(partes[:-2])
                pontuacao = int(partes[-2])
                data = partes[-1]
                ranking.append((nome, pontuacao, data))
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:5] 
    except FileNotFoundError:
        return []

"""
def telaGameOver(janela,pontuacao):
    teclado = janela.get_keyboard()
    nome = ""
    while True:
        janela.set_background_color(0,0,0)
        janela.draw_text("Game Over", janela.width/2, janela.height/2, size=28, color=(142,50,0), font_name="Arial", bold=False, italic=False)
        janela.draw_text(nome,janela.width/2-30,janela.height/2-30, size=28, color=(142,50,0),font_name="Arial")
        janela.update()"""