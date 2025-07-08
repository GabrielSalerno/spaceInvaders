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