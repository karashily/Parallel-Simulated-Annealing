import random as random
from numpy import floor

class Chip():
    def __init__(self, rows, cols, cells, conns, netlist):

        # initialize object constants:
        self.rowsNo = rows
        self.colsNo = cols
        self.cellsNo = cells
        self.netsNo = conns
        self.netlist = netlist

        # initialize object variables:
        self.area = self.rowsNo * self.colsNo

        self.cellLoc={}
        self.resetCellLoc()

        self.cellNetIncidence()

        # Calculate the current total cost:
        self.calcHpCost()

    def resetCellLoc(self):
        # Empty the current location dict:
        self.cellLoc={}

        # create random locations:
        indices = random.sample(range(self.area), self.cellsNo)
        randomlocs =  list(range(self.area)[i] for i in indices)

        # resent all locations to their random locations:
        for i in range(self.cellsNo):
            y = int(floor(randomlocs[i]*1.0 / self.colsNo))
            x = int(randomlocs[i] - y * self.colsNo)
            self.cellLoc[i] = (x,y)

    def calcBoundingBox(self, net_ID):
        rows = []
        cols = []

        # Loop over all cells in the net
        for cell in self.netlist[net_ID]:
            cols.append(self.cellLoc[cell][0])
            rows.append(self.cellLoc[cell][1])

        # find the left most, right most, highest and lowest cells in the net:
        # Then calculate the bounding box dimension:
        delta_y = max(rows) - min(rows)
        delta_x = max(cols) - min(cols)

        return delta_x + delta_y

    def calcHpCost(self):
        self.totCost=0
        for net in range(self.netsNo):
            self.totCost += self.calcBoundingBox(net)

    def subCalcHpCost(self,i,j):
        affectedNets = []

        # Find the nets affected by this change:
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