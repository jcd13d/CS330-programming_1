import matplotlib.pyplot as plt
import os
import datetime
import sys
import numpy as np
import json


def read_data(file):
    """
    Return dictionary of probabilities and days for each probability level
    """
    with open(file, "r") as f:
        x = f.read().split("\n\n")

    prob = x[0].split("\n")
    days = x[1].split("\n")

    prob = [float(x) for x in prob]
    # days = [float(x) for x in days]

    N = len(prob) / 4
    assert N % 4 == 0
    N = int(N)

    p_data = {}
    d_data = {}
    for i, p, in enumerate((0.1, 0.3, 0.5, 0.7)):
        p_data[p] = prob[i * N:N * (i + 1)]
        d_data[p] = days[i * N:N * (i + 1)]

    return p_data, d_data


def infected_count(probabilities, output_list):
    for probability, data in probabilities.items():
        output = {"probability": probability}
        data = np.array(data)

        output["infected_node_count"] = int(np.sum(data > 0))

        output_list.append(output)


def avg_time_to_infect(days_till_infect, output_list):
    for probability, data in days_till_infect.items():
        data = np.array(data)
        output = {"probability": probability}
        data[data != 'inf']
        mean = np.mean(data[data != 'inf'].astype('float64'))
        output["mean_days_to_infect"] = float(mean)
        output_list.append(output)


def probability_dist_plot(probabilities, graph, path=None, show=False):
    plt.figure(figsize=(4.5, 3))
    for probability, data in probabilities.items():
        data = sorted(data, reverse=True)
        plt.plot(np.linspace(0, len(data), len(data)), data, label="p = {0}".format(probability))
    plt.legend()
    plt.title("Probability Distribution for Infection: {0}".format(graph))
    plt.ylabel("Probability of Infection")
    plt.xlabel("Nodes")
    plt.grid(True, which='both')
    plt.tight_layout()

    if show:
        plt.show()
    if path is not None:
        plt.savefig(os.path.join(path, "pdist_{0}.jpg".format(graph)))

    plt.close()


def histogram_days(days_till_infect, graph, path=None, show=False):
    max_ = 0
    for probability, data in days_till_infect.items():
        data = np.array(data)
        data = np.round(data[data != 'inf'].astype('float64')).astype('int')
        max_ = np.max(data) if np.max(data) > max_ else max_

    plt.figure(figsize=(4, 3))
    for probability, data in days_till_infect.items():
        data = np.array(data)
        data = np.round(data[data != 'inf'].astype('float64')).astype('int')
        plt.hist(data, alpha=0.7, bins=np.linspace(0, max_, max_), label="p = {0}".format(probability))
        # plt.hist(data, alpha=0.7, label="p = {0}".format(probability))
        if (probability == 0.3) | (probability == 0.7):
            plt.title("Average Day of Infection: {0}".format(graph))
            plt.xlabel("Day Infected")
            plt.ylabel("Number of Nodes")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            if show:
                plt.show()
            if path is not None:
                plt.savefig(os.path.join(path, "histogram_{0}_{1}.jpg".format(graph, probability)))
                plt.close()
            plt.figure(figsize=(4, 3))


def main(args=[]):
    file = args[0]

    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    title = time + "_" + os.path.basename(file).split(".")[0]
    path = os.path.join("/Users/justindiemmanuele/Documents/school/MS/CS330/programming_1/executions", title)
    os.makedirs(path)

    master_output = {title: []}

    p, d = read_data(file)

    infected_count(p, master_output[title])
    probability_dist_plot(p, os.path.basename(file)[:-11], path=path)
    avg_time_to_infect(d, master_output[title])
    histogram_days(d, os.path.basename(file)[:-11], path=path)

    with open(os.path.join(path, "output.json"), "w") as f:
        json.dump(master_output, f)


# TODO: need to subtract 1 day from each because of source
if __name__ == "__main__":
    main(sys.argv[1:])
