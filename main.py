from numpy import mean
import os
import time
import chip
import placer



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
    print('Done.')
    print('Dimension of the chip: ' , rowsNo , 'x', colsNo)
    print('Number of cells = ', cellsNo)
    print('Number of nets = ', connsNo)

    return new_chip




# get the file address:
inputFile = input('Input File Location: ')

# Load the chip information:
chip = loadInput(inputFile)

# Create a simulated annealing based placement
SA = placer.Placer(chip, 5*10**5)

# Optimize the placement:
t0 = time.time()
cost =  SA.anneal()
t1 = time.time()

# Display the result:
print('Placement Done for chip at', inputFile)
print('with final cost:', cost)
print('Time elapsed:' , t1 - t0)

