# Because the graph is ordered after being converted to a matrix,
# and the node contains 0, so do not use -1 when calculating the row and column
# The ordered matrix corresponds to the unique number of the node. For example,
# if the out-degree and in-degree of node 10 are required, the parameter 10 needs to be passed in.
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.MultiDiGraph()  # multiple directed graph

# open file
# f_entity = open('dataset/entity2id.txt', 'r')
# f_relation = open('dataset/relation2id.txt', 'r')

f_train = open('dataset/train2id.txt', 'r')

save = open('temp.txt', 'w')

tot = (int)(f_train.readline())
gprah_data = []
for i in range(tot):
    content = f_train.readline()
    if len(content) != 1:
        line = content.strip().split()
        gprah_data.append(line)



# print(len(gprah_data))

# G.clear()
# f_train = open('dataset/train2id.txt', 'r')
# all_train = f_train.readlines()
new_train, feature_1, feature_2, weight, relation, entity, tail = [], [], [], [], [], [], []

# clear_dataset(all_train, new_train)

# print(new_train)
for train in gprah_data:
    if len(train) != 1 and len(train) != "":
        feature_1.append(train[0])
        feature_2.append(train[1])
        weight.append(train[2])

# for i in weight:
#     if i not in relation:
#         relation.append(i)
#
# for n in feature_1:
#     if n not in entity:
#         entity.append(n)
#
# for t in feature_2:
#     if t not in entity:
#         entity.append(t)
#
# entity = sorted(entity)
# relation = sorted(relation)
#
#
# for e in entity:
#     G.add_node(e)

# for i in range(len(gprah_data)):
#     print(gprah_data[i])
# for index in range(len(entity)):
#     G.add_edge(entity[index], )
# G.clear()
for edge in gprah_data:
    if len(edge) != 1:
        G.add_weighted_edges_from([(edge[0], edge[1], int(edge[2]))], weight=int(edge[2]))
        # G.add_edge(edge[0], edge[1])

# n_entity = nx.number_of_nodes(G)
# n_edge = nx.number_of_edges(G)
# n_relation = len(relation)

# return n_entity, n_relation, n_edge

# print(n_entity, n_edge, n_relation)

pos = nx.spring_layout(G, k=10)

# degree = nx.degree_histogram(G)
# x = range(len(degree))
# y = [z/float(sum(degree)) for z in degree]

nx.draw(G, pos=pos, with_labels=True)

# As_1 = nx.adjacency_matrix(G, weight=None)  # Ignore weights when converting to matrix 'weight=None'
# A_1 = As_1.todense()
# result = np.sum(A_1, axis=1)
# result_1 = np.sum(A_1, axis=0)
#
# arr_result = np.array(result)
# arr_result_1 = np.array(result_1)
#
# in_degree = np.sum(arr_result_1) / nx.number_of_nodes(G)
# out_degree = np.sum(arr_result) / nx.number_of_nodes(G)
#
# print(in_degree, out_degree)
plt.show()






