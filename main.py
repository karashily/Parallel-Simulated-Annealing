from numpy import mean
import os
import time
from multiprocessing import Process,Value,Lock,Manager,Lock

import chip as chip_class
import placer as placer_class
import copy


if __name__ == "__main__":
    with Manager() as manager:
        # Benchmarks = ['Examples/cm138a.txt',
        # 'Examples/cm150a.txt',
        # 'Examples/cm151a.txt',
        # 'Examples/cm162a.txt',
        # 'Examples/alu2.txt',
        # 'Examples/C880.txt',
        # 'Examples/e64.txt',
        # 'Examples/apex1.txt',
        # 'Examples/cps.txt',
        # 'Examples/paira.txt',
        # 'Examples/pairb.txt',
        # 'Examples/apex4.txt']
        Benchmarks = ['Examples/alu2.txt']
        # threadsNo = 
        # Main loop over all benchmarks:
        for inputFile in Benchmarks:
            chip = chip_class.Chip.loadChip(inputFile)
            costs = []
            times = []

            threadsNos = [1,2,4,8]
            T, sigma = placer_class.Placer.initParam(20000, chip)
            c = copy.deepcopy(chip)
            for threadsNo in threadsNos:
                for _ in range(5):
                    SAs = []
                    SA = placer_class.Placer(chip, 5*10**5 / threadsNo)

                    stateLock = Lock()
                    results = manager.dict()
                    
                    processes = []
                    for i in range(threadsNo):
                        p = Process(target=SA.anneal, args=(stateLock, chip, T, sigma, i, results))
                        processes.append(p)
                    
                    t0 = time.time()
                    for p in processes:    
                        p.start()
                    for p in processes:
                        p.join()
                    t1 = time.time()
                    t = t1 - t0

                    cost = results[0]
                    for i in range(threadsNo):
                        if(results[i] < cost):
                            cost = results[i]
                    costs.append(cost)
                    times.append(t)
                    chip = c

                print('Placement Done for chip:', inputFile, "with threadsNo", threadsNo)
                print('avg cost =', mean(costs))
                print('avg time elapsed =' , mean(times))
                costs = []
                times = []