import sys
import random

############################

# DO NOT CHANGE THIS PART!!

############################

def readGraph(input_file):
    with open(input_file, 'r') as f:
        raw = [line.split(',') for line in f.read().splitlines()]

    N = int(raw[0][0])
    print(raw)
    print(N)
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

def model_outbreak(N, s, adj_list):
    # Again, you are given N, s, and the adj_list
    # You can also call your BFS algorithm in this function,
    # or write other functions to use here.
    # Return two lists of size n, where each entry represents one vertex:
    prob_infect = [0]*N
    # the probability that each node gets infected after a run of the experiment
    avg_day = ['inf']*N
    # the average day of infection for each node
    # (you can write 'inf' for infinity if the node is never infected)
    # The code will write this information to a single text file.
    # If you do not name this file at the command prompt, it will be called 'outbreak_output.txt'.
    # The first N lines of the file will have the probability infected for each node.
    # Then there will be a single space.
    # Then the following N lines will have the avg_day_infected for each node.


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
