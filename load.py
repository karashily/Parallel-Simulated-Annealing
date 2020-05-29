''' This module imports the input information from an input file.'''

import chip_class as chip_cls

def load_input(filename, verbose = 0):

    print('='*80)
    print('Loading', filename, '...')

    # Initializing variables:
    net_list =[]
    net_blocks = []
    num_cells = 0
    num_conns = 0
    num_rows  = 0
    num_cols  = 0

    # Openning the input file:
    f = open(filename, "r")

    # Reading the content of the file:
    file_content = f.readlines()

    # pars the first line of the input line that includes:
    # the number of cells to be placed, the number of connections between the
    # cells, and the number of rows and columns upon which the circuit should be
    # placed.
    first_line = file_content[0].split()

    num_cells = int(first_line[0])
    num_conns = int(first_line[1])
    num_rows  = int(first_line[2])
    num_cols  = int(first_line[3])

    # Loop over the 2nd line to the last line of the file to populate the
    # net list info:
    for net in range(1,num_conns+1):

        # Clear the net_list temporary container:
        net_blocks = []

        # Read the line in the input file associated with net list "net":
        net_info =  file_content[net].split()

        # the first number in the line is the number of blocks
        net_num_block = int(net_info[0])

        # Append the blocks to the net block list:
        for i in range(1, net_num_block+1):
            net_blocks.append(int(net_info[i]))

        # Append this net to the master net list:
        net_list.append(net_blocks)

    # Create the chip object using the loaded information:
    new_chip  = chip_cls.chip(num_rows, num_cols, num_cells, num_conns, net_list)

    # Display the imported data:
    print('Done.')

    if verbose == 1:
        print('Dimension of the chip: ' , num_rows ,'x',num_cols)
        print('Number of cells = ',num_cells)
        print('Number of nets = ', num_conns)
        print('.'*80)



    return new_chip

if __name__ == "__main__":

    input_adress = 'Examples/cm138a.txt'
    chip1 = load_input(input_adress, verbose =1)
