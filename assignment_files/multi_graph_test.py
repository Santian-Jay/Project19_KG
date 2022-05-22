import tkinter
from tkinter import Frame
import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

G = nx.MultiDiGraph()  # multiple directed graph


def clear_dataset(dataset, new):
    G.clear()
    new.clear()
    for i in dataset:
        first = i.strip('\n')  # delete '\n'
        second = first.split()  # delete 'space'
        new.append(second)  # add data into list


def get_degree(graph):
    result = 0
    As_1 = nx.adjacency_matrix(graph, weight=None)   #Ignore weights when converting to matrix 'weight=None'
    print(As_1)
    A_1 = As_1.todense()
    print(A_1)
    result = np.sum(A_1, axis=1)
    result_1 = np.sum(A_1, axis=0)

    arr_result = np.array(result)
    arr_result_1 = np.array(result_1)

    print("out degree： \n", result)  # out degree list
    print("in degree： ", result_1)  #in degree list
    print("average in degree： ", np.sum(arr_result_1) / nx.number_of_nodes(graph))  # in degree list
    print("average out degree： ", np.sum(arr_result) / nx.number_of_nodes(graph))  # out degree list

    #print("node {} out degree： {}\n".format(node, arr_result[node][0]))  # out degree of specified node, if index include '0', then don't need -1
    #print("node {} in degree： {}".format(node, arr_result_1[0][node]))  # in degree of specified node

    ave_indegree, ave_outdegree = (np.sum(arr_result_1) / nx.number_of_nodes(graph)), (np.sum(arr_result) / nx.number_of_nodes(graph))
    return ave_indegree, ave_outdegree


def draw_distribution(graph, distributionFrame):
    result = 0
    As_1 = nx.adjacency_matrix(graph, weight=None)   #Ignore weights when converting to matrix 'weight=None'
    print(As_1)
    A_1 = As_1.todense()
    print(A_1)
    result = np.sum(A_1, axis=1)
    result_1 = np.sum(A_1, axis=0)

    arr_result = np.array(result)
    arr_result_1 = np.array(result_1)
    graph = sns.kedplot(arr_result, arr_result_1, shade=True)
    
    print("out degree： \n", result)  # out degree list
    print("in degree： ", result_1)  #in degree list
    print("average in degree： ", np.sum(arr_result_1) / nx.number_of_nodes(graph))  # in degree list
    print("average out degree： ", np.sum(arr_result) / nx.number_of_nodes(graph))  # out degree list

    #print("node {} out degree： {}\n".format(node, arr_result[node][0]))  # out degree of specified node, if index include '0', then don't need -1
    #print("node {} in degree： {}".format(node, arr_result_1[0][node]))  # in degree of specified node

    ave_indegree, ave_outdegree = (np.sum(arr_result_1) / nx.number_of_nodes(graph)), (np.sum(arr_result) / nx.number_of_nodes(graph))
    return ave_indegree, ave_outdegree

    #get the indegree and outdegree value from multigraph
    #indegree1=multi_graph.result
    #outdegree2=multi_graph.result_1
    #ax=sns.kdeplot(indegree1, shade=True)
    #c=sns.kdeplot(outdegree2, shade=True)


def draw_graph(new_entity, new_relation, new_train, graphFrame):
    feature_1, feature_2, weight, train_1, train_node = [], [], [], [], []

    for train in new_train:
        if len(train) != 1:
            feature_1.append(int(train[0]))
            feature_2.append(int(train[1]))
            weight.append(int(train[2]))

    for entity in new_entity:
        if len(entity) != 1:
            G.add_node(entity[1])

    for train in new_train:
        if len(train) != 1:
            G.add_weighted_edges_from([(train[0], train[1], int(train[2]))], weight=int(train[2]))   # Adding edges to multiple directed weight graphs

    pos = nx.spring_layout(G, k=10)

    print("graph has：{} deges".format(nx.number_of_edges(G)))    # print number of edge
    print("graph has：{} nodes".format(nx.number_of_nodes(G)))    # print number of node

    degree = nx.degree_histogram(G)       # Get the sequence of degree distributions of all nodes in the graph
    x = range(len(degree))
    y = [z/float(sum(degree)) for z in degree]
    nx.draw(G, pos=pos, with_labels=True)
    ax = plt.gca()
    for e in G.edges:
        ax.annotate("",
                    xy=pos[e[0]], xycoords='data',
                    xytext=pos[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle="-", color="0.5",
                                    shrinkA=5, shrinkB=5,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3, rad=rrr".replace('rrr', str(0.3*e[2])
                                                                            ),
                                    ),
                    )

    get_degree(G)
    frame1 = tkinter.Frame(graphFrame)
    frame1.pack()
    f = plt.figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    plt.axis('off')

    nx.draw_networkx(G, pos=pos, ax=a)
    xlim = a.get_xlim()
    ylim = a.get_ylim()

    canvas = FigureCanvasTkAgg(f, master=frame1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def data_only_graph(new_entity, new_relation, new_train):
    feature_1, feature_2, weight, train_1, train_node = [], [], [], [], []

    for train in new_train:
        if len(train) != 1:
            feature_1.append(int(train[0]))
            feature_2.append(int(train[1]))
            weight.append(int(train[2]))

    for entity in new_entity:
        if len(entity) != 1:
            G.add_node(entity[1])

    for train in new_train:
        if len(train) != 1:
            G.add_weighted_edges_from([(train[0], train[1], int(train[2]))], weight=int(train[2]))   # Adding edges to multiple directed weight graphs

    pos = nx.spring_layout(G, k=10)

    print("graph has：{} deges".format(nx.number_of_edges(G)))    # print number of edge
    print("graph has：{} nodes".format(nx.number_of_nodes(G)))    # print number of node

    degree = nx.degree_histogram(G)       # Get the sequence of degree distributions of all nodes in the graph

