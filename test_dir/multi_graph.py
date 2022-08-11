# Because the graph is ordered after being converted to a matrix,
# and the node contains 0, so do not use -1 when calculating the row and column
# The ordered matrix corresponds to the unique number of the node. For example,
# if the out-degree and in-degree of node 10 are required, the parameter 10 needs to be passed in.
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
import seaborn as sns
import pandas as pd

G = nx.MultiDiGraph()  # multiple directed graph

# open file
f_entity = open('../subgraph_v1/entity2id.txt', 'r')
f_relation = open('../subgraph_v1/relation2id.txt', 'r')
f_train = open('../subgraph_v1/train2id.txt', 'r')

# read all content
# data = f.read()
# print(data)   #end=''Do not print newline spaces，print(data, end='')
# #process file
all_entity = f_entity.readlines()
all_relation = f_relation.readlines()
all_train = f_train.readlines()


new_entity, new_relation, new_train, feature_1, feature_2, weight, train_1, train_node = [], [], [], [], [], [], [], []

def clear_dataset(dataset, new):
    for i in dataset:
        first = i.strip('\n')  # delete '\n'
        second = first.split()  # delete 'space'
        new.append(second)  # add data into list

clear_dataset(all_entity, new_entity)
new_data = clear_dataset(all_relation, new_relation)
clear_dataset(all_train, new_train)

print(new_train[0][0])


for train in new_train:
    if len(train) != 1:
        feature_1.append(int(train[0]))
        feature_2.append(int(train[1]))
        weight.append(int(train[2]))
#print(feature_1,feature_2,weight)

#print(new_relation)
#print(new_entity)
# for feature in feature_1:
#     G.add_node(feature)

for entity in new_entity:
    if len(entity) != 1:
        #print(data[1])
        G.add_node(entity[1])
        #G.add_node()

# for t in new_train:
#     if len(t) != 1:
#         train_1.append(t)
#
# print(len(train_1))

for train in new_train:
    if len(train) != 1:
        # G.add_weighted_edges_from([(train[0], train[1], train[2])], weight=float(train[2]))
        G.add_weighted_edges_from([(train[0], train[1], int(train[2]))], weight=int(train[2]))   # Adding edges to multiple directed weight graphs
        # print(train[0], train[1], train[2])
        # G.add_weighted_edges_from([(train[0], train[1], int(train[2]))], attr=train[2])
        # G.add_edge(train[0], train[1], weight=int(train[2]))

# df = pd.DataFrame({'f1': feature_1, 'f2': feature_2, 'weight': weight})
# print(df)
#
# G = nx.from_pandas_edgelist(df=df, source='f1', target='f2', edge_attr='weight')
#
# nodes = len(feature_1)
# print("长度是{}", nodes)

#useful code
pos = nx.spring_layout(G, k=10)

# pos = nx.get_edge_attributes(G, 'pos')
# nx.draw(G, pos, with_labels=True)
# labels = {e: G.edges[e]['weight'] for e in G.edges}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# labels = {e: G.edges[e]['weight'] for e in G.edges}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)


#
# for train in new_train:
#     if len(train) != 1:
#         #G.add_edge(train[0], train[1])
#         G.add_weighted_edges_from(train[0], train[1], train[2])
#         #print(train[0], train[1], train[2])

print("图的边共有：{}".format(nx.number_of_edges(G)))    # print number of edge
print("图的点共有：{}".format(nx.number_of_nodes(G)))    # print number of node
# print("The subgraphs of the graph：{}".format(nx.number_connected_components(G)))    # Print the number of connected subgraphs of the graph, Directed graph cannot be used

# print degree of node 10
# print(G.degree('10'))

degree = nx.degree_histogram(G)       # Get the sequence of degree distributions of all nodes in the graph
x = range(len(degree))
y = [z/float(sum(degree)) for z in degree]

# plt.loglog(x, y, color='blue', linewidth=2)  # Plot the degree distribution curve on a log-log axis

# nx.draw(G, pos, with_labels=True)

# testing code
# labels = {e: G.edges[e][weight] for e in G.edges}
# nx.draw(G, pos, with_labels=True, edge_labels=labels)
# labels = nx.get_edge_attributes(G, 'weight')
# print(len(labels))
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#
# labels = nx.get_edge_attributes(G,'weight')
# labels = {e: G.edges[e]['weight'] for e in G.edges}
# print(labels.keys())
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)


# useful code
# nx.draw(G, pos, with_labels=True)

# print duplicate edges
# ax = plt.gca()
# for e in G.edges:
#     ax.annotate("",
#                 xy=pos[e[0]], xycoords='data',
#                 xytext=pos[e[1]], textcoords='data',
#                 arrowprops=dict(arrowstyle="-", color="0.5",
#                                 shrinkA=5, shrinkB=5,
#                                 patchA=None, patchB=None,
#                                 connectionstyle="arc3, rad=rrr".replace('rrr', str(0.3*e[2])
#                                                                         ),
#                                 ),
#                 )

# As = nx.adjacency_matrix(G)
# print(As)
#
# A = As.todense()
# print(A)

def get_degree(graph, node):
    result = 0
    As_1 = nx.adjacency_matrix(graph, weight=None)   #Ignore weights when converting to matrix 'weight=None'
    # print(As_1)
    A_1 = As_1.todense()
    print(A_1)
    result = np.sum(A_1, axis=1)
    result_1 = np.sum(A_1, axis=0)

    new_arr = np.array(A_1)
    # print(type(new_arr))
    # print(new_arr)
    outd = np.sum(new_arr, axis=1)
    print(type(outd))
    print(outd)
    # ax = sns.kdeplot(outd)
    ind = np.sum(new_arr, axis=0)
    print(type(ind))
    print(ind)
    # sns.kdeplot(ind, ax=ax)

    # save_path = 'image/kde.png'
    # plt.savefig(save_path)
    # 可用代码
    data = pd.DataFrame({'indegree':ind, 'outdegree':outd})
    sns.kdeplot(data=data)

    arr_result = np.array(result)
    arr_result_1 = np.array(result_1)


    print(arr_result)
    print(arr_result_1)
    # tria = [list(map(int, result.split())) for  _ in range(len(arr_result))]

    print("out degree： \n", result)  # out degree list
    print("in degree： ", result_1)  #in degree list
    # print("average in degree： ", np.sum(arr_result_1) / nx.number_of_nodes(graph))  # in degree list
    # print("average out degree： ", np.sum(arr_result) / nx.number_of_nodes(graph))  # out degree list
    #
    # print("node {} out degree： {}\n".format(node, arr_result[node][0]))  # out degree of specified node, if index include '0', then don't need -1
    # print("node {} in degree： {}".format(node, arr_result_1[0][node]))  # in degree of specified node

get_degree(G, 10)
# -------------------------------------------------------------------------
# add node
# G.add_nodes_from([1, 2, 3, 4, 5])
# add edge
# G.add_edges_from([(1,2), (1,3), (2,3), (2,4), (3,5), (4,5)])

#sub graph
# sub_g = G.subgraph(['10', '11', '12'])
# nx.draw(sub_g, pos, node_size=800, edge_color='r', node_color='r', with_labels=True)
#
# # Get the nodes and edges of the subgraph to make a new graph
# train_1 = sub_g.edges()
# train_node = sub_g.nodes()
# print(train_1, train_node)
# print(sub_g.nodes(data=True))
# #drew graph
# nx.draw(G, node_size=500, with_labels=True)
# -------------------------------------------------------------------------
# print(get_Degrees(G, 10))





plt.show()
