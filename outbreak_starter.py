import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

############################

# DO NOT CHANGE THIS PART!!

############################

def readGraph(input_file):
    with open(input_file, 'r') as f:
        raw = [line.split(',') for line in f.read().splitlines()]

    N = int(raw[0][0])
    # print(raw)
    # print(N)
    sin = raw[1]
    s = []
    for st in sin:
        s.append(int(st))
    adj_list = []
    for line in raw[2:]:
        if line == ['-']:
            adj_list.append([])
        else:
            adj_list.append([int(index) for index in line])
    return N, s, adj_list


def writeOutput(output_file, prob_infect, avg_day):
    with open(output_file, 'w') as f:
        for i in prob_infect:
            f.write(str(i) + '\n')
        f.write('\n')
        for i in avg_day:
            f.write(str(i) + '\n')

 

def Run(input_file, output_file):
    N, s, adj_list = readGraph(input_file)
    prob_infect, avg_day =   model_outbreak(N, s, adj_list)
    writeOutput(output_file, prob_infect, avg_day)



def  BFS(N, s, adj_list):
    level = ['x']*N
    #######################################

    # COPY YOUR BFS CODE FROM PART 1 HERE

    ########################################
    discovered = N*[False]
    discovered[s] = True

    L = [[s]]
    i = 0
    level[s]=0

    while len(L[i]) != 0:
        L.append([])
        for node in L[i]:
            for neighbor in adj_list[node]:
                if not discovered[neighbor]:
                    discovered[neighbor] = True
                    L[i+1].append(neighbor)
                    level[neighbor] = i + 1
        i += 1

    return level

#######################################

# WRITE YOUR SOLUTION IN THIS FUNCTION

########################################


def viz_graph(adj_list, show=True, save=None, levels=None):

    g_format = ["{0} ".format(i) + " ".join(map(str, x)) for i, x in enumerate(adj_list)]
    G = nx.parse_adjlist(g_format, nodetype=int, create_using=nx.DiGraph)
    # G = nx.parse_adjlist(g_format, nodetype=int, create_using=nx.Graph)

    if levels is not None:
        color_map = ['blue'] * len(adj_list)
        for i, line in enumerate(nx.readwrite.adjlist.generate_adjlist(G)):
            if levels[int(line.split(" ")[0])] != 'x':
                color_map[i] = 'red'
                # print("colored ", line)
    else:
        color_map = None

    nx.draw(G, with_labels=True, node_color=color_map)

    if show:
        plt.show()

    if save is not None:
        plt.savefig(save)


def GenRndInstance(adj_list, probability):
    new_adj_list = []

    for vertex, adj_nodes in enumerate(adj_list):
        new_adj_list.append([])
        for adj_node in adj_nodes:
            if vertex == 0:
                active = True
            else:
                active = random.random() <= probability
            if active:
                new_adj_list[vertex].append(adj_node)

    return new_adj_list



def model_outbreak(N, s, adj_list):
    # Again, you are given N, s, and the adj_list
    # You can also call your BFS algorithm in this function,
    # or write other functions to use here.
    # Return two lists of size n, where each entry represents one vertex:
    # prob_infect = [0]*N
    # the probability that each node gets infected after a run of the experiment
    # the average day of infection for each node
    # (you can write 'inf' for infinity if the node is never infected)
    # The code will write this information to a single text file.
    # If you do not name this file at the command prompt, it will be called 'outbreak_output.txt'.
    # The first N lines of the file will have the probability infected for each node.
    # Then there will be a single space.
    # Then the following N lines will have the avg_day_infected for each node.

    iterations = 1000
    probabilities = (0.1, 0.3, 0.5, 0.7)

    prob_infect = []
    avg_day = []

    for probability in probabilities:
        infect = [[] for i in range(N)]
        day = [[] for i in range(N)]
        for i in range(iterations):
            rnd_adj_list = adj_list
            rnd_adj_list = [[i + 1 for i in row] for row in rnd_adj_list]
            rnd_adj_list.insert(0, [])
            for source in s:
                rnd_adj_list[0].append(source + 1)      # add 1 because we increased the node numbers by 1 w insert

            rnd_adj_list = GenRndInstance(rnd_adj_list, probability=probability)

            # bfs = BFS(N=len(adj_list), s=0, adj_list=adj_list)
            levels = BFS(N=len(rnd_adj_list), s=0, adj_list=rnd_adj_list)
            for i, dist in enumerate(levels):
                if (dist != 'x') and (i != 0):
                    infect[i - 1].append(1.0)
                    # TODO is this distance supposed to be indexed from 1 or 0 (we added a source node)
                    day[i - 1].append(dist)
                elif dist == 'x':
                    infect[i - 1].append(0.0)

        # infect = np.array(infect).mean(1, dtype=np.float64)
        infect = np.mean(np.array(infect), axis=1, dtype=np.float64)
        # print(infect)
        for i, (row_day, row_infect) in enumerate(zip(day, infect)):
            # infect[i] = np.mean((row_infect))
            if len(row_day) > 0:
                day[i] = np.mean(list(row_day))
            else:
                day[i] = "inf"

        prob_infect.extend(infect)
        avg_day.extend(day)


    # viz_graph(rnd_adj_list, show=True, levels=levels)
    # viz_graph(adj_list, show=True)
    # print(infect)

    return prob_infect, avg_day



############################

# DO NOT CHANGE THIS PART!!

############################


# read command line arguments and then run
def main(args=[]):
    filenames = []

    #graph file
    if len(args)>0:
        filenames.append(args[0])
        input_file = filenames[0]
    else:
        print()
        print('ERROR: Please enter file names on the command line:')
        print('>> python outbreak.py graph_file.txt output_file.txt')
        print()
        return

    # output file
    if len(args)>1:
        filenames.append(args[1])
    else:
        filenames.append('outbreak_output.txt')
    output_file = filenames[1]

    Run(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])    
