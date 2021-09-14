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
        for index, row in enumerate(self.rows):
            self.rows[index] = row[0].split(";")
            self.rows[index] = list(filter(None, self.rows[index]))
    
    def writeTempCsv(self):
        tempString = ""

        print(self.rows)
        for row in self.rows:
            for el in row:
                print(el)
                tempString += f"{el};"
            tempString = tempString[:-1]
            tempString += "\n"

        f = open(f"{self.tempFileName}.csv", "w")
        f.write(tempString)
        f.close()

        pass


class Conjunto:
    def __init__(self):
        self.n = []
        self.E = []
        self.fon = []
        self.FO = [[]]
        self.t = [[]]

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
    pass

if __name__ == "__main__":
    main()
    