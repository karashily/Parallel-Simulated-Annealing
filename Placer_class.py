''' This module defines a placer class that is designed based on simulated
annealing optimization of a half-parameter bounding box cost function.'''
import random as RND
from numpy import exp, std, mean,log, absolute, floor


class sa_placer_agent():
    def __init__(self, chip_obj, max_iterations, verbose=0):
        self.verbose = verbose
        self.temp_schedule = []
        self.max_iter = max_iterations
        self.T = 0
        self.num_iter = 0
        self.chip = chip_obj
        self.current_delta_cost = 0
        self.sigma=0
        self.max_param_sample = 20000
        self.no_change = 0
        self.accepted = True
        self.num_rejection = 0
        self.num_acceptance = 0
        self.epsilon = 1
        self.rejection=0
        self.last_good_move = 0

    def param_initialization(self):
        '''
        The initialization is based on improvements suggested by the following
        Paper:
        VLSI cell placement Techniques
        K shahkoor and P. mazumder
        '''

        # Kai0 is the initial desired acceptance probability:
        self.Kai0 = .90

        # Initializing variables:
        DELTA_C=[]
        DELTA_C_PLUS = []

        m2=0
        m1=0

        for i in range(self.max_param_sample):
            cell_i, cell_j, delta_cost = self.random_swap()
            DELTA_C.append(delta_cost)

            if delta_cost > 0:
                DELTA_C_PLUS.append(delta_cost)
                m2 += 1
            elif delta_cost <=0:
                m1 += 1

        self.sigma = round(std(DELTA_C),10)


        DELTA_C_PLUS_AVG = mean(DELTA_C_PLUS)

        self.T = DELTA_C_PLUS_AVG/ \
        (log(m2*1.0/(m2*self.Kai0  - (1-self.Kai0 )*m1)))

        #self.T =20*self.sigma

        if self.verbose > 0:
            print('-'*50)
            print('SA Initial Parameters:')
            print("Average Delta C+ of sample:" , DELTA_C_PLUS_AVG)
            print("Sigma of sample: ", self.sigma)
            print('# Cost decreasing samples:', m1)
            print('# Cost increasing samples:', m2)
            print('Initial temperature T0:' , self.T)
            print('-'*50)

            if self.verbose > 1:
                print('(!) Visulizing the initial state.')
                print('(>) Close the figure to continue ...')
                self.chip.draw_chip()

    def update_temperature(self):
        ''' Temperature update based on Huang et al. [1986]
        '''
        if self.rejection > 0.01 * self.max_iter:
            self.T=self.T*100
        else:
            if round(self.T, 10)*(1.0*self.current_delta_cost/self.sigma**2)<100:

                self.T = self.T * exp(round(self.T, 10)* \
                (1.0*self.current_delta_cost/self.sigma**2))
            else:
                self.T = self.T * exp(100)

    def random_swap(self):

        [i,j] = RND.sample(range(self.chip.num_cells),2)

        delta_cost = self.chip.swap_delta_cost(i,j)

        return i,j, delta_cost

    def make_move(self):

        cell_i, cell_j, delta_cost = self.random_swap()

        if delta_cost < 0:
            self.last_good_move = self.num_iter

        if self.T < 0.000000000000001:
            if delta_cost > 0:
                check = 0
            else:
                check = 1
        else:
            check = exp(-delta_cost*(self.num_iter - self.last_good_move)/round(self.T,14))
        

        if RND.uniform(0, 1) <= check:
            self.chip.commit_swap_cells(cell_i,cell_j)
            self.current_delta_cost = delta_cost
            self.accepted = True
            self.rejection=0
        else:
            self.accepted = False
            self.rejection +=1

        self.update_temperature()

    def anneal(self):
        self.param_initialization()

        if self.verbose > 0:
            if self.num_iter % int(floor(0.01 * self.max_iter)) == 0:
                print('>>> Temp:', self.T,', Iter:', self.num_iter,\
                ', Cost:' , self.chip.total_cost)
                
        while (self.num_iter <= self.max_iter) and \
         (self.no_change <= 0.05 * self.max_iter):


            self.make_move()

            # Book keeping section for SA:
            self.num_iter += 1

            if self.accepted == False:
                self.num_rejection += 1
            else:
                self.num_acceptance += 1

            if (absolute(self.current_delta_cost) < self.epsilon):
                self.no_change += 1
            else:
                self.no_change = 0


            # Printing every 1% of the whole process ...
            if self.verbose > 0:
                if self.num_iter % int(floor(0.01 * self.max_iter)) == 0:
                    print('>>> Temp:', self.T,', Iter:', self.num_iter,\
                    ', Cost:' , self.chip.total_cost)

            if self.verbose > 1:
                if self.num_iter % int(floor(0.1 * self.max_iter)) == 0:
                    print('(!) Visulizing the current state.')
                    print('(>) Close the figure to continue ...')
                    self.chip.draw_chip()

        # After SA:
        if self.verbose > 1:
            print('(!) Visulizing the current state.')
            print('(>) Close the figure to continue ...')
            self.chip.draw_chip()

        return self.chip.total_cost
