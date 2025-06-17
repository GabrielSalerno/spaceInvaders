from datetime import date

def criarRanking(pontuacao):
    arquivo = open("ranking.txt","w")
    nome = input()
    data= date.today()
    arquivo.write(f"{nome} {pontuacao} {data}")