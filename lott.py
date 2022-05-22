# This method calculates the out-degree and in-degree of a
# node by converting the graph into a matrix, where the out-degree
# is the sum of the rows and the in-degree is the sum of the columns
# matrices are ordered
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.MultiDiGraph()   #multiple directed graph

# G.add_nodes_from([1, 2, 3, 4, 5, 6])
#
# G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (3, 6), (5, 6)])

G.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f'])

G.add_edges_from([('a', 'b'), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('c', 'f'), ('e', 'f')])

pos = nx.random_layout(G)

plt.subplot(251)
nx.draw(G, pos, node_size=500, with_labels=True)
plt.subplot(252)
nx.draw(G, pos, node_size=400, with_labels=True, node_color="r")
plt.subplot(253)
nx.draw(G, pos, node_size=600, with_labels=True, node_color="g")
plt.subplot(254)
nx.draw(G, pos, node_size=500, with_labels=True, node_color="b")

As = nx.adjacency_matrix(G)
print(As)

A = As.todense()
print(A)

# Convert a matrix into a 2D array to get values
arr_A = np.array(A)
print("一个元素: ", arr_A[0][1])

print(G.degree('e'))


def get_degree(graph, node):
    As_1 = nx.adjacency_matrix(graph)    #Convert the graph to an adjacency matrix
    A_1 = As_1.todense()                 #Convert the matrix to the form of a 2D array
    result = np.sum(A_1, axis=1)         #get the rows of the matrix, row is out degree
    result_1 = np.sum(A_1, axis=0)       #get the columns of the matrix, column is in degree

    arr_result = np.array(result)        #Convert row to 2D array
    arr_result_1 = np.array(result_1)    #Convert column to 2D array

    #print("out degree is： ", np.sum(arr))   #Sum of rows, row is out-degree, column is in-degree

    print("out degree： \n", result)  # out degree list
    print("in degree： ", result_1)  #in degree list
    print("average in degree： ", np.sum(arr_result_1) / nx.number_of_nodes(graph))  # average in degree
    print("average out degree： ", np.sum(arr_result) / nx.number_of_nodes(graph))   # average out degree

    #print("{} out degree： {}\n".format(node, arr_result[node - 1][0]))  # out degree of specified node, if index don't include '0', then need -1
    #print("{} in degree： {}".format(node, arr_result_1[0][node - 1]))  # in degree of specified node

#print(get_degree(G, 1))

get_degree(G, 'e')


print("The graph has: {} edges".format(nx.number_of_edges(G)))    # print number of edge
print("The graph has: {} nodes".format(nx.number_of_nodes(G)))    # print number of node

plt.show()    # print graph

# X = [[1, 2, 3],
#      [4, 5, 6],
#      [7, 8, 9]]
#
# Y = [[9, 8, 7],
#      [6, 5, 4],
#      [3, 2, 1]]
#
# result = [[X[i][j] + Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]
#
# for r in result:
#     print(r)