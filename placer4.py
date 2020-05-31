import random
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
        self.lastBadMove = 0

    def initParam(self):
        '''
        The initialization is based on improvements suggested by the following
        Paper:
        VLSI cell placement Techniques
        K shahkoor and P. mazumder
        '''

        # Kai0 is the initial desired acceptance probability:
        Kai0 = .90

        # Initializing variables:
        DELTA_C=[]
        DELTA_C_PLUS = []

        m2=0
        m1=0

        for i in range(self.maxParamSample):
            cell_i, cell_j, deltaCost = self.getRandomSwap()
            self.deltaCostArr.append(deltaCost)

            if deltaCost > 0:
                DELTA_C_PLUS.append(deltaCost)
                m2 += 1
            elif deltaCost <=0:
                m1 += 1

        self.sigma = std(self.deltaCostArr)


        DELTA_C_PLUS_AVG = mean(DELTA_C_PLUS)

        # self.T = DELTA_C_PLUS_AVG / (log(m2 /(m2 * Kai0 - (1 - Kai0) * m1)))

        P = 0.9
        k = -3 / log(P)
        self.T = k*self.sigma


        # print('-'*50)
        # print('SA Initial Parameters:')
        # print("Average Delta C+ of sample:" , DELTA_C_PLUS_AVG)
        # print("Sigma of sample: ", self.sigma)
        # print('# Cost decreasing samples:', m1)
        # print('# Cost increasing samples:', m2)
        # print('Initial temperature T0:' , self.T)
        # print('-'*50)

        
    def updateT(self):
        ''' Temperature update based on Huang et al. [1986] '''
        if self.consectiveRejection > 0.01 * self.maxIterNo:
            self.T=self.T*100
        else:
            if (self.T * self.currentDeltaCost / self.sigma**2 < 100):
                self.T = self.T * exp(self.T * self.currentDeltaCost / self.sigma**2)
            else:
                self.T = self.T * exp(100)

    def getRandomSwap(self):
        [i,j] = random.sample(range(self.chip.cellsNo),2)
        deltaCost = self.chip.swapDeltaCost(i,j)
        return i,j, deltaCost

    def move(self):
        cell_i, cell_j, deltaCost = self.getRandomSwap()
        
        # self.deltaCostArr.append(deltaCost)
        # self.sigma = std(self.deltaCostArr)

        if(deltaCost <= 0):
            self.lastGoodMove = self.iter

        if self.T < 0.000000000000001:
            if deltaCost > 0:
                check = 0
            else:
                check = 1
        else:
            # check = exp(-deltaCost/self.T)
            check = exp(-deltaCost*(self.iter-self.lastGoodMove)/(self.iter-self.lastBadMove + 0.0000001)/self.T)

        if random.uniform(0, 1) <= check:
            self.chip.commitSwap(cell_i,cell_j)
            self.currentDeltaCost = deltaCost
            self.accepted = True
            self.consectiveRejection = 0
            self.lastBadMove = self.iter
        else:
            self.accepted = False
            self.consectiveRejection +=1

        self.updateT()

    def anneal(self):
        self.initParam()

        # print('>>> Temp:', self.T,', Iter:', self.iter, ', Cost:' , self.chip.totCost)
                
        while (self.iter <= self.maxIterNo) and (self.noChangeNo <= 0.05 * self.maxIterNo):
            self.move()
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
           
        return self.chip.totCost
