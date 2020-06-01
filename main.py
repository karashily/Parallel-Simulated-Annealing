from numpy import mean
import os
import time
import copy
import ctypes
import sys
from multiprocessing import Process, Manager, Lock, Value

import chip as cs
import simulated_annealing as sa


if __name__ == "__main__":
	with Manager() as manager:
		inputFile = input("Please Enter the testcase filename: ")
		threadsNums = [1, 2, 4, 8]
		runsPerTest = 20
		chip = cs.Chip.loadChip(inputFile)
		for threadsNo in threadsNums:
			costs = []
			times = []
			for _ in range(runsPerTest):
				newChip = copy.deepcopy(chip)
				SAs = []
				SA = sa.simAnnealing(chip, 5*10**5 / threadsNo)

				T, sigma = sa.simAnnealing.initParam(20000, chip)
				stateLock = Lock()
				result = Value(ctypes.c_int, lock=True)
				
				processes = []
				for _ in range(threadsNo):
					p = Process(target=SA.anneal, args=(stateLock, newChip, T, sigma, result))
					processes.append(p)

				t0 = time.time()
				for p in processes:    
					p.start()
				for p in processes:
					p.join()
				t1 = time.time()
				t = t1 - t0

				costs.append(result.value)
				times.append(t)

			print('Placement Done for chip:', inputFile, "with threadsNo", threadsNo)
			print('avg cost =', mean(costs))
			print('avg time =', mean(times))