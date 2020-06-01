import random, copy
from numpy import exp, std, mean,log, absolute, floor

class simAnnealing():
    def __init__(self, chip, maxIter):
        self.maxIterNo = maxIter
        self.T = 0
        self.iter = 0
        self.chip = chip
        self.currentDeltaCost = 0
        self.sigma=0
        self.maxParamSample = 20000
        self.noChangeNo = 0
        self.accepted = True
        self.epsilon = 1
        self.deltaCostArr = []
        self.lastGoodMove = 0
        self.finalCost = 0
    
    @classmethod
    def initParam(cls, maxParamSample, chip):
        deltaCostVec = []
        for _ in range(maxParamSample):
            _, _, deltaCost = cls.getInitRandomSwap(chip)
            deltaCostVec.append(deltaCost)

        sigma = std(deltaCostVec)

        P = 0.9
        k = -3 / log(P)
        T = k * sigma

        return T, sigma
    
    @classmethod
    def getInitRandomSwap(cls, chip):
        [i,j] = random.sample(range(chip.cellsNo) ,2)
        deltaCost = chip.swapDeltaCost(i,j)
        return i, j, deltaCost

    def updateT(self):
        if (self.T * self.currentDeltaCost / (self.sigma**2 + 0.00001) < 100):
            self.T = self.T * exp(self.T * self.currentDeltaCost / (self.sigma**2 + 0.00001)) 
        else:
            self.T = self.T * exp(100)

    def getRandomMove(self):
        [i,j] = random.sample(range(self.chip.cellsNo) ,2)
        copiedChip = copy.deepcopy(self.chip)
        copiedChip.swapCells(i, j)
        newCost = copiedChip.calcHpCost()
        return newCost, i, j

    def evaluateAndCommit(self, deltaCost, i, j):
        if self.T < 0.000000001:
            if deltaCost > 0:
                check = 0
            else:
                check = 1
        elif deltaCost < 0:
            check = 1
        else:
            check = exp(-1 * deltaCost * (self.iter - self.lastGoodMove) / self.T)

        if check >= random.uniform(0, 1):
            self.chip.commitSwap(i, j)
            self.currentDeltaCost = deltaCost
            self.accepted = True
        else:
            self.accepted = False


    def anneal(self, lock, chip, T, sigma, result):
        self.chip = chip
        self.T = T
        self.sigma = sigma

        while (self.iter <= self.maxIterNo) and (self.noChangeNo <= 0.05 * self.maxIterNo):
            newCost, firstCell, secondCell = self.getRandomMove()        
            lock.acquire()
            deltaCost = newCost - self.chip.totCost
            self.evaluateAndCommit(deltaCost, firstCell, secondCell)
            lock.release()

            if(deltaCost <= 0):
                self.lastGoodMove = self.iter

            if (absolute(self.currentDeltaCost) <= self.epsilon):
                self.noChangeNo += 1
            else:
                self.noChangeNo = 0
            
            self.updateT()            
            self.iter += 1
        if self.chip.totCost < result.value or result.value == 0:
            with result.get_lock():
                result.value = self.chip.totCost