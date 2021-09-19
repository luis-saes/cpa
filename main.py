import pandas as pd
import csv
import math

'''
Friedman aligned-ranks test; 
Friedman two-way analysis of variance by ranks; 
Iman-Davenport test; 
Quade test

link da tabela com os role Alpha: https://www.medcalc.org/manual/chi-square-table.php
link da tabela z: http://www.z-table.com/
'''

class Planilha:
    def __init__(self) -> None:
        self.fileName = "cpa"
        self.tempFileName = "tempCpa"
        self.rows = []
        #estou assumindo que nosso alpha vai ser 0.05
        #grau de liberdade = k - 1 = 8 - 1 = 7 
        # k é 8 pq tem 8 colunas, eu entendi assim
        self.alpha = 0.05
        self.k = 8
        self.chiSquareValue = 14.067
        self.positiveZTable = [[ None, 0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09],
[0.00, 0.50000, 0.50399, 0.50798, 0.51197, 0.51595, 0.51994, 0.52392, 0.52790, 0.53188, 0.53586],
[0.10, 0.53983, 0.54380, 0.54776, 0.55172, 0.55567, 0.55962, 0.56356, 0.56749, 0.57142, 0.57535],
[0.20, 0.57926, 0.58317, 0.58706, 0.59095, 0.59483, 0.59871, 0.60257, 0.60642, 0.61026, 0.61409],
[0.30, 0.61791, 0.62172, 0.62552, 0.62930, 0.63307, 0.63683, 0.64058, 0.64431, 0.64803, 0.65173],
[0.40, 0.65542, 0.65910, 0.66276, 0.66640, 0.67003, 0.67364, 0.67724, 0.68082, 0.68439, 0.68793],
[0.50, 0.69146, 0.69497, 0.69847, 0.70194, 0.70540, 0.70884, 0.71226, 0.71566, 0.71904, 0.72240],
[0.60, 0.72575, 0.72907, 0.73237, 0.73565, 0.73891, 0.74215, 0.74537, 0.74857, 0.75175, 0.75490],
[0.70, 0.75804, 0.76115, 0.76424, 0.76730, 0.77035, 0.77337, 0.77637, 0.77935, 0.78230, 0.78524],
[0.80, 0.78814, 0.79103, 0.79389, 0.79673, 0.79955, 0.80234, 0.80511, 0.80785, 0.81057, 0.81327],
[0.90, 0.81594, 0.81859, 0.82121, 0.82381, 0.82639, 0.82894, 0.83147, 0.83398, 0.83646, 0.83891],
[1.00, 0.84134, 0.84375, 0.84614, 0.84849, 0.85083, 0.85314, 0.85543, 0.85769, 0.85993, 0.86214],
[1.10, 0.86433, 0.86650, 0.86864, 0.87076, 0.87286, 0.87493, 0.87698, 0.87900, 0.88100, 0.88298],
[1.20, 0.88493, 0.88686, 0.88877, 0.89065, 0.89251, 0.89435, 0.89617, 0.89796, 0.89973, 0.90147],
[1.30, 0.90320, 0.90490, 0.90658, 0.90824, 0.90988, 0.91149, 0.91309, 0.91466, 0.91621, 0.91774],
[1.40, 0.91924, 0.92073, 0.92220, 0.92364, 0.92507, 0.92647, 0.92785, 0.92922, 0.93056, 0.93189],
[1.50, 0.93319, 0.93448, 0.93574, 0.93699, 0.93822, 0.93943, 0.94062, 0.94179, 0.94295, 0.94408],
[1.60, 0.94520, 0.94630, 0.94738, 0.94845, 0.94950, 0.95053, 0.95154, 0.95254, 0.95352, 0.95449],
[1.70, 0.95543, 0.95637, 0.95728, 0.95818, 0.95907, 0.95994, 0.96080, 0.96164, 0.96246, 0.96327],
[1.80, 0.96407, 0.96485, 0.96562, 0.96638, 0.96712, 0.96784, 0.96856, 0.96926, 0.96995, 0.97062],
[1.90, 0.97128, 0.97193, 0.97257, 0.97320, 0.97381, 0.97441, 0.97500, 0.97558, 0.97615, 0.97670],
[2.00, 0.97725, 0.97778, 0.97831, 0.97882, 0.97932, 0.97982, 0.98030, 0.98077, 0.98124, 0.98169],
[2.10, 0.98214, 0.98257, 0.98300, 0.98341, 0.98382, 0.98422, 0.98461, 0.98500, 0.98537, 0.98574],
[2.20, 0.98610, 0.98645, 0.98679, 0.98713, 0.98745, 0.98778, 0.98809, 0.98840, 0.98870, 0.98899],
[2.30, 0.98928, 0.98956, 0.98983, 0.99010, 0.99036, 0.99061, 0.99086, 0.99111, 0.99134, 0.99158],
[2.40, 0.99180, 0.99202, 0.99224, 0.99245, 0.99266, 0.99286, 0.99305, 0.99324, 0.99343, 0.99361],
[2.50, 0.99379, 0.99396, 0.99413, 0.99430, 0.99446, 0.99461, 0.99477, 0.99492, 0.99506, 0.99520],
[2.60, 0.99534, 0.99547, 0.99560, 0.99573, 0.99585, 0.99598, 0.99609, 0.99621, 0.99632, 0.99643],
[2.70, 0.99653, 0.99664, 0.99674, 0.99683, 0.99693, 0.99702, 0.99711, 0.99720, 0.99728, 0.99736],
[2.80, 0.99744, 0.99752, 0.99760, 0.99767, 0.99774, 0.99781, 0.99788, 0.99795, 0.99801, 0.99807],
[2.90, 0.99813, 0.99819, 0.99825, 0.99831, 0.99836, 0.99841, 0.99846, 0.99851, 0.99856, 0.99861],
[3.00, 0.99865, 0.99869, 0.99874, 0.99878, 0.99882, 0.99886, 0.99889, 0.99893, 0.99896, 0.99900],
[3.10, 0.99903, 0.99906, 0.99910, 0.99913, 0.99916, 0.99918, 0.99921, 0.99924, 0.99926, 0.99929],
[3.20, 0.99931, 0.99934, 0.99936, 0.99938, 0.99940, 0.99942, 0.99944, 0.99946, 0.99948, 0.99950],
[3.30, 0.99952, 0.99953, 0.99955, 0.99957, 0.99958, 0.99960, 0.99961, 0.99962, 0.99964, 0.99965],
[3.40, 0.99966, 0.99968, 0.99969, 0.99970, 0.99971, 0.99972, 0.99973, 0.99974, 0.99975, 0.99976],
[3.50, 0.99977, 0.99978, 0.99978, 0.99979, 0.99980, 0.99981, 0.99981, 0.99982, 0.99983, 0.99983],
[3.60, 0.99984, 0.99985, 0.99985, 0.99986, 0.99986, 0.99987, 0.99987, 0.99988, 0.99988, 0.99989],
[3.70, 0.99989, 0.99990, 0.99990, 0.99990, 0.99991, 0.99991, 0.99992, 0.99992, 0.99992, 0.99992],
[3.80, 0.99993, 0.99993, 0.99993, 0.99994, 0.99994, 0.99994, 0.99994, 0.99995, 0.99995, 0.99995],
[3.90, 0.99995, 0.99995, 0.99996, 0.99996, 0.99996, 0.99996, 0.99996, 0.99996, 0.99997, 0.99997],
[4.00, 0.99997, 0.99997, 0.99997, 0.99997, 0.99997, 0.99997, 0.99998, 0.99998, 0.99998, 0.99998],
[4.10, 0.99998, 0.99998, 0.99998, 0.99998, 0.99998, 0.99998, 0.99998, 0.99998, 0.99999, 0.99999],
[4.20, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999],
[4.30, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999, 0.99999],
[4.40, 0.99999, 0.99999, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000],
[4.50, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000],
[4.60, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000],
[4.70, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000],
[4.80, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000],
[4.90, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000]]
        self.negativeZTable = [[ None, 0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09],
[-4.90, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
[-4.80, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
[-4.70, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
[-4.60, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
[-4.50, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
[-4.40, 0.00001, 0.00001, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
[-4.30, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001],
[-4.20, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001],
[-4.10, 0.00002, 0.00002, 0.00002, 0.00002, 0.00002, 0.00002, 0.00002, 0.00002, 0.00001, 0.00001],
[-4.00, 0.00003, 0.00003, 0.00003, 0.00003, 0.00003, 0.00003, 0.00002, 0.00002, 0.00002, 0.00002],
[-3.90, 0.00005, 0.00005, 0.00004, 0.00004, 0.00004, 0.00004, 0.00004, 0.00004, 0.00003, 0.00003],
[-3.80, 0.00007, 0.00007, 0.00007, 0.00006, 0.00006, 0.00006, 0.00006, 0.00005, 0.00005, 0.00005],
[-3.70, 0.00011, 0.00010, 0.00010, 0.00010, 0.00009, 0.00009, 0.00008, 0.00008, 0.00008, 0.00008],
[-3.60, 0.00016, 0.00015, 0.00015, 0.00014, 0.00014, 0.00013, 0.00013, 0.00012, 0.00012, 0.00011],
[-3.50, 0.00023, 0.00022, 0.00022, 0.00021, 0.00020, 0.00019, 0.00019, 0.00018, 0.00017, 0.00017],
[-3.40, 0.00034, 0.00032, 0.00031, 0.00030, 0.00029, 0.00028, 0.00027, 0.00026, 0.00025, 0.00024],
[-3.30, 0.00048, 0.00047, 0.00045, 0.00043, 0.00042, 0.00040, 0.00039, 0.00038, 0.00036, 0.00035],
[-3.20, 0.00069, 0.00066, 0.00064, 0.00062, 0.00060, 0.00058, 0.00056, 0.00054, 0.00052, 0.00050],
[-3.10, 0.00097, 0.00094, 0.00090, 0.00087, 0.00084, 0.00082, 0.00079, 0.00076, 0.00074, 0.00071],
[-3.00, 0.00135, 0.00131, 0.00126, 0.00122, 0.00118, 0.00114, 0.00111, 0.00107, 0.00104, 0.00100],
[-2.90, 0.00187, 0.00181, 0.00175, 0.00169, 0.00164, 0.00159, 0.00154, 0.00149, 0.00144, 0.00139],
[-2.80, 0.00256, 0.00248, 0.00240, 0.00233, 0.00226, 0.00219, 0.00212, 0.00205, 0.00199, 0.00193],
[-2.70, 0.00347, 0.00336, 0.00326, 0.00317, 0.00307, 0.00298, 0.00289, 0.00280, 0.00272, 0.00264],
[-2.60, 0.00466, 0.00453, 0.00440, 0.00427, 0.00415, 0.00402, 0.00391, 0.00379, 0.00368, 0.00357],
[-2.50, 0.00621, 0.00604, 0.00587, 0.00570, 0.00554, 0.00539, 0.00523, 0.00508, 0.00494, 0.00480],
[-2.40, 0.00820, 0.00798, 0.00776, 0.00755, 0.00734, 0.00714, 0.00695, 0.00676, 0.00657, 0.00639],
[-2.30, 0.01072, 0.01044, 0.01017, 0.00990, 0.00964, 0.00939, 0.00914, 0.00889, 0.00866, 0.00842],
[-2.20, 0.01390, 0.01355, 0.01321, 0.01287, 0.01255, 0.01222, 0.01191, 0.01160, 0.01130, 0.01101],
[-2.10, 0.01786, 0.01743, 0.01700, 0.01659, 0.01618, 0.01578, 0.01539, 0.01500, 0.01463, 0.01426],
[-2.00, 0.02275, 0.02222, 0.02169, 0.02118, 0.02068, 0.02018, 0.01970, 0.01923, 0.01876, 0.01831],
[-1.90, 0.02872, 0.02807, 0.02743, 0.02680, 0.02619, 0.02559, 0.02500, 0.02442, 0.02385, 0.02330],
[-1.80, 0.03593, 0.03515, 0.03438, 0.03362, 0.03288, 0.03216, 0.03144, 0.03074, 0.03005, 0.02938],
[-1.70, 0.04457, 0.04363, 0.04272, 0.04182, 0.04093, 0.04006, 0.03920, 0.03836, 0.03754, 0.03673],
[-1.60, 0.05480, 0.05370, 0.05262, 0.05155, 0.05050, 0.04947, 0.04846, 0.04746, 0.04648, 0.04551],
[-1.50, 0.06681, 0.06552, 0.06426, 0.06301, 0.06178, 0.06057, 0.05938, 0.05821, 0.05705, 0.05592],
[-1.40, 0.08076, 0.07927, 0.07780, 0.07636, 0.07493, 0.07353, 0.07215, 0.07078, 0.06944, 0.06811],
[-1.30, 0.09680, 0.09510, 0.09342, 0.09176, 0.09012, 0.08851, 0.08691, 0.08534, 0.08379, 0.08226],
[-1.20, 0.11507, 0.11314, 0.11123, 0.10935, 0.10749, 0.10565, 0.10383, 0.10204, 0.10027, 0.09853],
[-1.10, 0.13567, 0.13350, 0.13136, 0.12924, 0.12714, 0.12507, 0.12302, 0.12100, 0.11900, 0.11702],
[-1.00, 0.15866, 0.15625, 0.15386, 0.15151, 0.14917, 0.14686, 0.14457, 0.14231, 0.14007, 0.13786],
[-0.90, 0.18406, 0.18141, 0.17879, 0.17619, 0.17361, 0.17106, 0.16853, 0.16602, 0.16354, 0.16109],
[-0.80, 0.21186, 0.20897, 0.20611, 0.20327, 0.20045, 0.19766, 0.19489, 0.19215, 0.18943, 0.18673],
[-0.70, 0.24196, 0.23885, 0.23576, 0.23270, 0.22965, 0.22663, 0.22363, 0.22065, 0.21770, 0.21476],
[-0.60, 0.27425, 0.27093, 0.26763, 0.26435, 0.26109, 0.25785, 0.25463, 0.25143, 0.24825, 0.24510],
[-0.50, 0.30854, 0.30503, 0.30153, 0.29806, 0.29460, 0.29116, 0.28774, 0.28434, 0.28096, 0.27760],
[-0.40, 0.34458, 0.34090, 0.33724, 0.33360, 0.32997, 0.32636, 0.32276, 0.31918, 0.31561, 0.31207],
[-0.30, 0.38209, 0.37828, 0.37448, 0.37070, 0.36693, 0.36317, 0.35942, 0.35569, 0.35197, 0.34827],
[-0.20, 0.42074, 0.41683, 0.41294, 0.40905, 0.40517, 0.40129, 0.39743, 0.39358, 0.38974, 0.38591],
[-0.10, 0.46017, 0.45620, 0.45224, 0.44828, 0.44433, 0.44038, 0.43644, 0.43251, 0.42858, 0.42465],
[-0.00, 0.50000, 0.49601, 0.49202, 0.48803, 0.48405, 0.48006, 0.47608, 0.47210, 0.46812, 0.46414]]


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
    
    def valueK(self):
        return len(self.rows[0].output)

    def valueB(self):
        return len(self.rows)

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


#pelo que eu entendi, os roles que tão ai em cima são usados por mais de um tipo de teste prarametrico
#inicio de coisas relacionadas apenas ao teste de Friedman

#calcula o valor de F de Friedman
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



#coisas relacionadas em caso de rejeição da hipotese nula
def citicalValue(planilha, conjunto):
       
    tailArea = planilha.alpha/(planilha.k * (planilha.k - 1))
    graphArea = 1 - tailArea
    if graphArea > 0.5:
        z = findTableValue(graphArea, planilha.positiveZTable)
    else: 
        z = findTableValue(graphArea, planilha.negativeZTable)
    b = conjunto.valueB()
    k = conjunto.valueK()
    return z*math.sqrt((b*k*(k+1))/6)
    


def findTableValue(graphArea, table):
    qtdRows = len(table)
    qtdColumns = len(table[0])
    for i in range(1, qtdRows):
        for j in range(1, qtdColumns):
            if table[i][j] > graphArea:
                return closest(table, i, j, graphArea)

def closest(table, i, j, graphArea):
    iAnterior, jAnterior = anterior(i, j, table)
    valorAtual = table[i][j]
    valorAnterior = table[iAnterior][jAnterior]

    diferencaAtual = modula(graphArea - valorAtual)
    diferencaAnterior = modula(graphArea - valorAnterior)

    if diferencaAnterior < diferencaAtual:
        return table[iAnterior][0] + table[0][jAnterior]
    else:
        return table[i][0] + table[0][j]
    
def modula(valor):
    if valor < 0:
        return valor *-1
    return valor

def anterior(i, j, table):
    maxJ = len(table[0])
    if j > 0:
        return i, j-1
    else:
        return i-1, maxJ

def rankAddSolution(array):
    array_copy = array.copy()
    for i in range(len(array)):
        array[i] = ( "S"+str(i)  , array[i])
    array_copy = sorted(array_copy)
    for indexi, i in enumerate(array_copy):
        for indexj, j in enumerate(array):
            if i == j[1]:
                array_copy[indexi] = array[indexj]
                array.pop(indexj)
    print("array_copy", array_copy)
    return array_copy


#fim de coisas relacionadas apenas ao teste de Friedman

def main():
    planilha = Planilha()
    conjuntos = planilha.build()
    matrix_ranks = []
    for conjunto in conjuntos:
        soma = soma_ranks(conjunto)
        f = calculateFriedman(conjunto, soma)
        if f >= planilha.chiSquareValue:
            print("rejeitada hipotese nula, aceita hipotese alternativa, pois f =", f, " o que é maior ou igual a", planilha.chiSquareValue)
            print(citicalValue(planilha, conjunto))
            print(soma)
            rankAddSolution(soma)
        else:
            print("aceita hipotese nula, rejeitada hipotese alternativa, pois f =", f, " o que é menor que", planilha.chiSquareValue)

    
        
    pass



if __name__ == "__main__":
    main()
    