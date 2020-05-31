from numpy import mean
import os
import time
import chip
import placer1
import placer2
import placer3
import placer4


def loadInput(filename):

    print('Loading', filename, '...',)

    # Reading the content of the file:
    content = open(filename, "r").readlines()

    # pars the first line of the input line that includes:
    # the number of cells to be placed, the number of connections between the
    # cells, and the number of rows and columns upon which the circuit should be
    # placed.
    firstLine = content[0].split()
    cellsNo = int(firstLine[0])
    connsNo = int(firstLine[1])
    rowsNo  = int(firstLine[2])
    colsNo  = int(firstLine[3])

    netlist =[]
    # Loop over the 2nd line to the last line of the file to populate the
    # net list info:
    for net in range(1, connsNo + 1):

        netBlocks = []

        # Read the line in the input file associated with net list "net":
        netInfo =  content[net].split()

        # the first number in the line is the number of blocks
        netBlockNo = int(netInfo[0])

        # Append the blocks to the net block list:
        for i in range(1, netBlockNo + 1):
            netBlocks.append(int(netInfo[i]))

        # Append this net to the master net list:
        netlist.append(netBlocks)

    # Create the chip object using the loaded information:
    new_chip = chip.Chip(rowsNo, colsNo, cellsNo, connsNo, netlist)

    # Display the imported data:
    # print('Done.')
    # print('Dimension of the chip: ' , rowsNo , 'x', colsNo)
    # print('Number of cells = ', cellsNo)
    # print('Number of nets = ', connsNo)

    return new_chip


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

# Main loop over all benchmarks:
for inputFile in Benchmarks:

    # Load the chip information:
    chip1 = loadInput(inputFile)
    chip2 = loadInput(inputFile)
    chip3 = loadInput(inputFile)
    chip4 = loadInput(inputFile)


    # Create a simulated annealing based placement
    SA1 = placer1.Placer(chip1, 5*10**5)
    SA2 = placer2.Placer(chip2, 5*10**5)
    SA3 = placer3.Placer(chip3, 5*10**5)
    SA4 = placer4.Placer(chip4, 5*10**5)

    cost1 = []
    cost2 = []
    cost3 = []
    cost4 = []

    time1 = []
    time2 = []
    time3 = []
    time4 = []

    # Optimize the placement:
    for i in range(50):
        t0 = time.time()
        cost =  SA1.anneal()
        cost1.append(cost)
        t1 = time.time()
        time1.append(t1-t0)
        
        t0 = time.time()
        cost =  SA2.anneal()
        cost2.append(cost)
        t1 = time.time()
        time2.append(t1-t0)
        
        t0 = time.time()
        cost =  SA3.anneal()
        cost3.append(cost)
        t1 = time.time()
        time3.append(t1-t0)
        
        t0 = time.time()
        cost =  SA4.anneal()
        cost4.append(cost)
        t1 = time.time()
        time4.append(t1-t0)
        

    # Display the result:
    print('Placement Done for chip at', inputFile)
    print('1 with final cost:', mean(cost1))
    print('2 with final cost:', mean(cost2))
    print('3 with final cost:', mean(cost3))
    print('4 with final cost:', mean(cost4))
    print('1 Time elapsed:' , mean(time1))
    print('2 Time elapsed:' , mean(time2))
    print('3 Time elapsed:' , mean(time3))
    print('4 Time elapsed:' , mean(time4))



# # get the file address:
# inputFile = input('Input File Location: ')

# # Load the chip information:
# chip1 = loadInput(inputFile)
# chip2 = loadInput(inputFile)
# chip3 = loadInput(inputFile)
# chip4 = loadInput(inputFile)


# # Create a simulated annealing based placement
# SA1 = placer1.Placer(chip1, 5*10**5)
# SA2 = placer2.Placer(chip2, 5*10**5)
# SA3 = placer3.Placer(chip3, 5*10**5)
# SA4 = placer4.Placer(chip4, 5*10**5)

# cost1 = []
# cost2 = []
# cost3 = []
# cost4 = []

# time1 = []
# time2 = []
# time3 = []
# time4 = []

# # Optimize the placement:
# for i in range(50):
#     t0 = time.time()
#     cost =  SA1.anneal()
#     cost1.append(cost)
#     t1 = time.time()
#     time1.append(t1-t0)
    
#     t0 = time.time()
#     cost =  SA2.anneal()
#     cost2.append(cost)
#     t1 = time.time()
#     time2.append(t1-t0)
    
#     t0 = time.time()
#     cost =  SA3.anneal()
#     cost3.append(cost)
#     t1 = time.time()
#     time3.append(t1-t0)
    
#     t0 = time.time()
#     cost =  SA4.anneal()
#     cost4.append(cost)
#     t1 = time.time()
#     time4.append(t1-t0)
    

# # Display the result:
# print('Placement Done for chip at', inputFile)
# print('1 with final cost:', mean(cost1))
# print('2 with final cost:', mean(cost2))
# print('3 with final cost:', mean(cost3))
# print('4 with final cost:', mean(cost4))
# print('1 Time elapsed:' , mean(time1))
# print('2 Time elapsed:' , mean(time2))
# print('3 Time elapsed:' , mean(time3))
# print('4 Time elapsed:' , mean(time4))

