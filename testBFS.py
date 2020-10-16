from breadth_first_search import BFS


if __name__ == "__main__":
    adj_list =  [[1,2], [0,2,3,4], [0,1,4,6,7], [1,4], [1,2,3,5], [4], [2,7], [2,6]]
    source = 0
    N = 8

    print(BFS(N, source, adj_list))