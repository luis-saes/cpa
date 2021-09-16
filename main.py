import pandas as pd
import csv

class Planilha:
    def __init__(self) -> None:
        self.fileName = "cpa"
        self.tempFileName = "tempCpa"
        self.rows = []

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
            print(row)
            self.rows[index] = row[0].split(";")
            self.rows[index] = list(filter(None, self.rows[index]))
    
    def writeTempCsv(self):
        tempString = ""

        print(self.rows)
        for row in self.rows:
            print(row)
            for el in row:
                tempString += f"{el};"
            tempString = tempString[:-1]
            tempString += "\n"

        f = open(f"{self.tempFileName}.csv", "w")
        f.write(tempString)
        f.close()

        pass
    
    def build(self):
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
                    print(i, row[i], row[i+1])
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

    def rankeia(self):
        rank = [[]]
        
        for row in self.FO:
            row_copy = sorted(row.copy())
            last = -1
            pos_first_last = -1
            for index,cell in row_copy:
                if cell == last:
                    continue
                    #\/
                qtd_repeted = index - pos_first_last
                # qtd_repeted
               
                pass

    

    

def main():
    planilha = Planilha()
    planilha.readCsv()
    planilha.clearRows()
    planilha.writeTempCsv()
    conjuntos = planilha.build()
    print("----------------------------------------------------------------------------")
    for conjunto in conjuntos:
        print("jkadfjkag")
        for row in conjunto.rows:
            print("linha", row.id, row.n, row.E, row.fon, row.output)
        print(conjunto.FOzero, conjunto.FO, conjunto.output)
    pass

if __name__ == "__main__":
    main()
    