import load as LD
import Placer_class as PLC
from numpy import mean
import os
import time


os.system('clear')

print('='*80)
print('Simulated Annealing Based VLSI Placement')
print('developed by: Arman Zaribafiyan')
print('='*80)

mode = input('Enter (1) for Benchmark, or (2) for Single Run: ')

print('Set Verbosity to:')
print('(0) Final results only.')
print('(1) Textual output.')
print('(2) Visual Output:')

visual = input('verbosity: ')

if int(mode) == 1:
    # Initializing variables and benchmarks:
    Benchmarks = ['Examples/cm138a.txt',
    'Examples/cm150a.txt',
    'Examples/cm151a.txt',
    'Examples/cm162a.txt',
    'Examples/alu2.txt',
    'Examples/C880.txt',
    'Examples/e64.txt',
    'Examples/apex1.txt',
    'Examples/cps.txt',
    'Examples/paira.txt',
    'Examples/pairb.txt',
    'Examples/apex4.txt']

    #Benchmarks = ['Examples/apex4.txt']
    cost_vec=[]

    # Main loop over all benchmarks:
    for  input_adress in Benchmarks:

        # Load the chip information:
        chip1 = LD.load_input(input_adress, verbose = 0)

        # Create a simulated annealing based placement
        sa_agent = PLC.sa_placer_agent(chip1, 5*10**5, verbose = int(visual))

        # Optimize the placement:
        t0 = time.time()

        final_cost =  sa_agent.anneal()

        t1=time.time()

        # Display the result:
        print('-'*50)
        print('Placement Done for chip at', input_adress)
        print('with final cost:', final_cost)
        print('Time elapsed:' , t1 - t0)

        # Store the cost for stats:
        cost_vec.append(final_cost)

    # Calculating the stats:
    AVG_cost = mean(cost_vec)

    # Display Final results:
    print('='*50)
    print("Experiment done with average cost:", AVG_cost)

elif int(mode)==2:

    # get the file address:
    input_adress = raw_input('Input File Location: ')

    # Load the chip information:
    chip1 = LD.load_input(input_adress, verbose=0)

    # Create a simulated annealing based placement
    sa_agent = PLC.sa_placer_agent(chip1, 5*10**5, verbose = int(visual))

    # Optimize the placement:
    t0 = time.time()

    final_cost =  sa_agent.anneal()

    t1 = time.time()
    # Display the result:
    print('-'*50)
    print('Placement Done for chip at', input_adress)
    print('with final cost:', final_cost)
    print('Time elapsed:' , t1 - t0)

else:
    print('Wrong input. BYE!')
