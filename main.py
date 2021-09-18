import pandas as pd
import csv


'''
Friedman aligned-ranks test; 
Friedman two-way analysis of variance by ranks; 
Iman-Davenport test; 
Quade test

link da tabela com os role Alpha: https://www.medcalc.org/manual/chi-square-table.php
'''

class Planilha:
    def __init__(self) -> None:
        self.fileName = "cpa"
        self.tempFileName = "tempCpa"
        self.rows = []
        #estou assumindo que nosso alpha vai ser 0.05
        #grau de liberdade = k - 1 = 8 - 1 = 7 
        self.chiSquareValue = 14.067

    def readCsv(self):
        with open(f"{self.fileName}.csv", "r", newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                self.rows.append(row)

    def clearRows(self):
        self.rows.pop(0)
        self.rows.pop(0)
        self.rows.pop(0)
        for index, row in enumerate(self.rows):

            if row[0] == 'pFO;;e':
                row.pop(0)
            self.rows[index] = row[0].split(";")
            self.rows[index] = list(filter(None, self.rows[index]))
    
    def writeTempCsv(self):
        tempString = ""

        for row in self.rows:
            for el in row:
                tempString += f"{el};"
            tempString = tempString[:-1]
            tempString += "\n"

        f = open(f"{self.tempFileName}.csv", "w")
        f.write(tempString)
        f.close()

        pass
    
    def build(self):

        self.readCsv()
        self.clearRows()
        rows = []
        fo0 = []
        fo = []
        conjuntos = []

        for row in self.rows:



            if row[0] == 'pt':
                fo0 = []
                fo = []
                fo0.append(float(row[1].replace(",", ".")))
                i = 2
                while i < 17:
                    fo.append(float(row[i].replace(",", ".")))
                    i += 2
            elif row[0] == 'vFO':
                fo0.append(float(row[1].replace(",", ".")))
                i = 2
                result = []
                while i <= 9:
                    result.append((fo[i-2],float(row[i].replace(",", "."))))
                    i += 1
                conjuntos.append(Conjunto(rows, fo0, fo, result))
                rows = []
            else:
                this_row = Row( int(row[0]), int(row[1]), int(row[2]), int(row[3]), [])
                output = []
                i = 4
                while i < 19:
                    row[i+1] = row[i+1].replace(",", ".")
                    output.append((int(row[i]), float(row[i+1])))
                    i = i+2
                this_row.output = output
                rows.append(this_row)
        return conjuntos
        


class Conjunto:
    def __init__(self, rows, FOzero, FO, output):
        self.rows = rows
        self.FOzero = FOzero
        self.FO = FO
        self.output = output

class Row:
    def __init__(self, id, n, E, fon, output):
        self.id = id
        self.n = n
        self.E = E
        self.fon = fon
        self.output = output

    
               

def filtra(row, choice):

    value_to_analise = []
    for output in row.output:
        value_to_analise.append(output[choice])
    return value_to_analise
    
def gera_posicoes(array):

    array_copy = sorted(array.copy())
    curretn_value = array_copy[0]
    pos_first_last = 0
    tam = len(array_copy)
    i = 0
    saida = []
    while i < tam:
        if array_copy[i] == curretn_value:
            i += 1
            continue
            #\/
        qtd_repeted = i - pos_first_last
        dividendo = 0
        for j in range(pos_first_last, i):
            dividendo += j + 1
        saida.append((curretn_value, dividendo/ qtd_repeted))
        curretn_value = array_copy[i]
        pos_first_last = i
        i += 1

    qtd_repeted = i - pos_first_last
    dividendo = 0
    for j in range(pos_first_last, i):
        dividendo += j + 1
    saida.append((curretn_value, dividendo/ qtd_repeted))
    return saida
        # qtd_repeted

#isso aqui retorna um array com a ordem de rankeamento que a linha que foi enserida aqui tinha
def rankeia(row):
    linha = filtra(row, 0)
    tuplas_rank = gera_posicoes(linha)
    array_com_rank = []
    for value in row.output:
        for tupla in tuplas_rank:
            if value[0] == tupla[0]:
                array_com_rank.append((tupla[1]))
                break
        else:
            print ("ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    return array_com_rank

#isso aqui retorna um array a soma do rank de um conjunto enserido aqui
def soma_ranks(conjunto):
    matrix_rank = []
    for row in conjunto.rows:
        matrix_rank.append(rankeia(row))

    tam = len(matrix_rank[0])
    soma_ranks_saida = [0] * tam
    for c in range(tam):
        for r in range(len(matrix_rank)):
            soma_ranks_saida[c] += matrix_rank[r][c]
    return soma_ranks_saida


def calculateFriedman(conjunto, soma_ranks):
    p2 = 0
    for num in soma_ranks:
        num = num*num
        p2 += num
    
    b = len(conjunto.rows)
    k = 8
    p1 = 12/(b*k*(k+1))
    p3 = 3*b*(k+1)
    return p1*p2-p3



def main():
    planilha = Planilha()
    conjuntos = planilha.build()
    matrix_ranks = []
    for conjunto in conjuntos:
        soma = soma_ranks(conjunto)
        f = calculateFriedman(conjunto, soma)
        if f >= planilha.chiSquareValue:
            print("rejeitada hipotese nula, aceita hipotese alternativa, pois f =", f, " o que é maior ou igual a", planilha.chiSquareValue)
        else:
            print("aceita hipotese nula, rejeitada hipotese alternativa, pois f =", f, " o que é menor que", planilha.chiSquareValue)

    
        
    pass



if __name__ == "__main__":
    main()
    