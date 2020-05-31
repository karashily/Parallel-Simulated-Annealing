import random, copy
from numpy import exp, std, mean,log, absolute, floor

class Placer():
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
        self.rejectNo = 0
        self.acceptNo = 0
        self.epsilon = 0.0000001
        self.consectiveRejection = 0
        self.deltaCostArr = []
        self.lastGoodMove = 0
        self.finalCost = 0
    
    @classmethod
    def initParam(cls, maxParamSample, chip):
        deltaCostVec = []
        for i in range(maxParamSample):
            cell_i, cell_j, deltaCost = cls.getInitRandomSwap(chip)
            deltaCostVec.append(deltaCost)

        sigma = std(deltaCostVec)

        P = 0.9
        k = -3 / log(P)
        T = k * sigma

        # print('SA Initial Parameters:')
        # print("Sigma of sample: ", sigma)
        # print('Initial temperature T0:' , T)
        return T, sigma
    
    @classmethod
    def getInitRandomSwap(cls, chip):
        [i,j] = random.sample(range(chip.cellsNo) ,2)
        deltaCost = chip.swapDeltaCost(i,j)
        return i, j, deltaCost

    def updateT(self):
        ''' Temperature update based on Huang et al. [1986] '''
        if self.consectiveRejection > 0.01 * self.maxIterNo:
            self.T=self.T*100
        else:
            if (self.T * self.currentDeltaCost / (self.sigma**2 + 0.00001) < 100):
                self.T = self.T * exp(self.T * self.currentDeltaCost / (self.sigma**2 + 0.00001)) 
            else:
                self.T = self.T * exp(100)

    def getRandomSwap(self):
        [i,j] = random.sample(range(self.chip.cellsNo) ,2)
        return i,j

    def move(self, lock):

        cell_i, cell_j = self.getRandomSwap()
        copiedChip = copy.deepcopy(self.chip)
        copiedChip.swapCells(cell_i, cell_j)
        newCost = copiedChip.calcHpCost()

        lock.acquire()
        deltaCost = newCost - self.chip.totCost
        
        self.deltaCostArr.append(deltaCost)
        if self.iter % int(floor(0.01 * self.maxIterNo)) == 0:
            self.sigma = std(self.deltaCostArr)

        if(deltaCost <= 0):
            self.lastGoodMove = self.iter

        if self.T < 0.000000000000001:
            if deltaCost > 0:
                check = 0
            else:
                check = 1
        else:
            check = exp(-deltaCost*(self.iter-self.lastGoodMove)/self.T)

        if random.uniform(0, 1) <= check:
            self.chip.commitSwap(cell_i,cell_j)
            self.currentDeltaCost = deltaCost
            self.accepted = True
            self.consectiveRejection = 0
        else:
            self.accepted = False
            self.consectiveRejection +=1
        lock.release()
        self.updateT()

    def anneal(self, lock, chip, T, sigma, i, results):
        self.chip = chip
        self.T = T
        self.sigma = sigma

        # print('>>> Temp:', self.T,', Iter:', self.iter, ', Cost:' , self.chip.totCost)
                
        while (self.iter <= self.maxIterNo) and (self.noChangeNo <= 0.05 * self.maxIterNo):
            self.move(lock)
            self.iter += 1

            if self.accepted == False:
                self.rejectNo += 1
            else:
                self.acceptNo += 1

            if (absolute(self.currentDeltaCost) <= self.epsilon):
                self.noChangeNo += 1
            else:
                self.noChangeNo = 0

            # if self.iter % int(floor(0.01 * self.maxIterNo)) == 0:
            #     print('>>> Temp:', self.T,', Iter:', self.iter, ', Cost:' , self.chip.totCost)

        results[i] = self.chip.totCost
        # return self.chip.totCost
