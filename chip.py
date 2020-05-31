import random as random
from numpy import floor

class Chip():
    def __init__(self, rows, cols, cells, conns, netlist):
        self.rowsNo = rows
        self.colsNo = cols
        self.cellsNo = cells
        self.netsNo = conns
        self.netlist = netlist

        self.area = self.rowsNo * self.colsNo
        self.cellLoc={}

        self.resetCellLoc()
        self.cellNetIncidence()
        self.calcHpCost()
    
    @classmethod
    def loadChip(cls, filename):
        print('Loading', filename, '.......',)
        content = open(filename, "r").readlines()
        firstLine = content[0].split()
        cellsNo = int(firstLine[0])
        connsNo = int(firstLine[1])
        rowsNo  = int(firstLine[2])
        colsNo  = int(firstLine[3])

        netlist =[]
        for net in range(1, connsNo + 1):
            netBlocks = []
            netInfo =  content[net].split()
            netBlockNo = int(netInfo[0])
            for i in range(1, netBlockNo + 1):
                netBlocks.append(int(netInfo[i]))
            netlist.append(netBlocks)

        newChip = cls(rowsNo, colsNo, cellsNo, connsNo, netlist)
        print('Done.....!')
        return newChip

    def resetCellLoc(self):
        self.cellLoc={}
        indices = random.sample(range(self.area), self.cellsNo)
        randomlocs =  list(range(self.area)[i] for i in indices)
        for i in range(self.cellsNo):
            y = int(floor(randomlocs[i]*1.0 / self.colsNo))
            x = int(randomlocs[i] - y * self.colsNo)
            self.cellLoc[i] = (x,y)

    def calcBoundingBox(self, netId):
        rows = []
        cols = []

        for cell in self.netlist[netId]:
            cols.append(self.cellLoc[cell][0])
            rows.append(self.cellLoc[cell][1])

        delta_y = max(rows) - min(rows)
        delta_x = max(cols) - min(cols)

        return delta_x + delta_y

    def calcHpCost(self):
        self.totCost=0
        for net in range(self.netsNo):
            self.totCost += self.calcBoundingBox(net)

    def subCalcHpCost(self,i,j):
        affectedNets = self.incidence[i] + self.incidence[j]
        affectedNets= list(set(affectedNets))

        cost = 0
        for net in affectedNets:
            cost += self.calcBoundingBox(net)
        return cost

    def swapCells(self,i,j):
        temp_1 = self.cellLoc[i]
        self.cellLoc[i] = self.cellLoc[j]
        self.cellLoc[j]= temp_1

    def commitSwap(self, i, j):
        self.totCost += self.swapDeltaCost(i,j)
        self.swapCells(i,j)


    def cellNetIncidence(self):
        self.incidence = {}
        for net in range(self.netsNo):
            for cell in self.netlist[net]:
                if cell in self.incidence.keys():
                    self.incidence[cell].append(net)
                else:
                    self.incidence[cell] = [net]

    def swapDeltaCost(self,i,j):
        self.swapCells(i,j)
        cost = self.subCalcHpCost(i,j)
        self.swapCells(i,j)
        return cost - self.subCalcHpCost(i,j)