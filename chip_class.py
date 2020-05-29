''' This module defines a chip object that contains information about its cells,
The size of the chip, the net lists and position of each cell on the chip.'''
import random as random
from numpy import floor
import networkx as nx
import matplotlib.pyplot as plt

class chip():
    def __init__(self, rows, cols, cells, conns, net_list):

        # initialize object constants:
        self.num_rows = rows
        self.num_cols = cols
        self.num_cells = cells
        self.num_nets = conns
        self.net_list = net_list

        # initialize object variables:
        self.area = self.num_rows * self.num_cols

        self.cell_location={}
        self.reset_cell_location()

        self.cell_net_incidence()

        # Calculate the current total cost:
        self.cost_half_perim()

        # Prepare for drawing the chip:
        self.pre_draw()

    def reset_cell_location(self):
        ''' This function resets the location of the cells to a randomly chosen
        location.'''

        # Empty the current location dict:
        self.cell_location={}

        # create random locations:
        indices = random.sample(xrange(self.area), self.num_cells)
        random_locations =  list(range(self.area)[i] for i in indices)

        # resent all locations to their random locations:
        for i in range(self.num_cells):
            y = int(floor(random_locations[i]*1.0 / self.num_cols))
            x = int(random_locations[i] - y * self.num_cols)
            self.cell_location[i] = (x,y)

    def calculate_bounding_box(self, net_ID):
        ''' This function calculates the dimensions of the bounding box for a
        particular net.'''

        rows = []
        cols = []

        # Loop over all cells in the net
        for cell in self.net_list[net_ID]:
            cols.append(self.cell_location[cell][0])
            rows.append(self.cell_location[cell][1])

        # find the left most, right most, highest and lowest cells in the net:
        # Then calculate the bounding box dimension:
        delta_y = max(rows) - min(rows)
        delta_x = max(cols) - min(cols)

        return delta_x + delta_y

    def cost_half_perim(self):

        ''' this function calculates the half perimeter cost for all nets'''

        self.total_cost=0

        for net in range(self.num_nets):
            self.total_cost += self.calculate_bounding_box(net)

    def subcost_half_perim(self,i,j):
        ''' This function is designed to calculate the half perimeter cost only
        for the nets affected by the swap of cell i and j'''

        nets_affected = []

        # Find the nets affected by this change:
        nets_affected = self.incidence[i] + self.incidence[j]

        nets_affected= list(set(nets_affected))

        current_net_aff_cost = 0


        for net in nets_affected:
            current_net_aff_cost += self.calculate_bounding_box(net)

        return current_net_aff_cost

    def swap_cells(self,i,j):
        '''This function swaps two cells'''

        temp_1 = self.cell_location[i]
        temp_2 = self.cell_location[j]

        self.cell_location[i]= temp_2
        self.cell_location[j]= temp_1

    def commit_swap_cells(self, i, j):
        ''' This function finalizes a cell swap by incorporating it into the
        cost function'''

        #update Cost
        self.total_cost += self.swap_delta_cost(i,j)

        # Do the swap:
        self.swap_cells(i,j)


    def cell_net_incidence(self):
        '''This function creates a dictionary of cells and the corresponding
        nets in which each cell appears. This is used to understand which nets
        are affected when a swap of a paricular cell is happening:'''

        self.incidence = {}

        for net in range(self.num_nets):
            for cell in self.net_list[net]:
                if cell in self.incidence.keys():
                    self.incidence[cell].append(net)
                else:
                    self.incidence[cell] = [net]

    def swap_delta_cost(self,i,j):
        ''' This function calculates the diference in cost after swapping 2
        cells. In its current form it calculates the whole cost function for all
        nets at each point. This can be improved a lot by only chaning the cost
        for the affected cells.'''

        # store the sub cost according to i and j before the swap
        current_cost = self.subcost_half_perim(i,j)

        # do the swap:
        self.swap_cells(i,j)

        # store the cost after the swap:
        future_cost = self.subcost_half_perim(i,j)

        # return everything back to its previous location:
        self.swap_cells(i,j)

        return future_cost - current_cost

    def pre_draw(self):
        ''' preprocess an edge-less networkx grid graph object based on the
        specifications of the chip.'''

        self.G = nx.grid_2d_graph(self.num_cols, self.num_rows)

        self.pos = dict( (n, n) for n in self.G.nodes() )

        self.G.remove_edges_from(self.G.edges())

    def draw_chip(self):
        ''' This fucntion draws the grid of the chip and highlights the location
        of different cells'''

        labels = {}

        for key in range(self.num_cells):
            labels[self.cell_location[key]]=key

        colors=[]
        for node in self.G.nodes():

            if node in self.cell_location.values():
                colors.append('#f2325f')
            else:
                colors.append('#A0CBE2')

        nx.draw_networkx(self.G, pos=self.pos, labels=labels,font_size=6,\
        node_size=150,node_color = colors)

        plt.axis('off')
        plt.show()

    def display(self):
        ''' For debigging perpusos displays the current state of the chip.'''
        
        print('Current Cell locations:')
        print(self.cell_location)

        print('The current cost:')
        print(self.total_cost)
