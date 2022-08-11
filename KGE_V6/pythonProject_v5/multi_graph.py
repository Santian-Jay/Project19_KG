import tkinter
from tkinter import Frame
import pandas as pd
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
    A_1 = As_1.todense()
    result = np.sum(A_1, axis=1)
    result_1 = np.sum(A_1, axis=0)

    arr_result = np.array(result)
    arr_result_1 = np.array(result_1)

    new_arr = np.array(A_1)   # covert matrix to array

    outddddd = np.sum(new_arr, axis=1)
    out_dddddata = pd.DataFrame({'outdegree': outddddd})
    sns.kdeplot(data=out_dddddata)
    save_path11 = 'dis_images/out-ddddd.png'
    plt.savefig(save_path11)
    plt.close()

    outdddd = np.sum(new_arr, axis=1)
    out_ddddata = pd.DataFrame({'outdegree': outdddd})
    sns.kdeplot(data=out_ddddata)
    save_path11 = 'dis_images/out-dddd.png'
    plt.savefig(save_path11)
    plt.close()

    outddd = np.sum(new_arr, axis=1)
    out_dddata = pd.DataFrame({'outdegree': outddd})
    sns.kdeplot(data=out_dddata)
    save_path11 = 'dis_images/out-ddd.png'
    plt.savefig(save_path11)
    plt.close()

    outdd = np.sum(new_arr, axis=1)
    out_ddata = pd.DataFrame({'outdegree': outdd})
    sns.kdeplot(data=out_ddata)
    save_path11 = 'dis_images/out-dd.png'
    plt.savefig(save_path11)
    plt.close()


    outd = np.sum(new_arr, axis=1)
    out_data = pd.DataFrame({'outdegree': outd})
    sns.kdeplot(data=out_data)
    save_path1 = 'dis_images/out-d.png'
    plt.savefig(save_path1)
    plt.close()


    ind = np.sum(new_arr, axis=0)
    in_data = pd.DataFrame({'indegree': ind, 'outdegree': outd})
    sns.kdeplot(data=in_data)
    save_path2 = 'dis_images/in-d.png'
    plt.savefig(save_path2)
    plt.close()

    ave_indegree, ave_outdegree = (np.sum(arr_result_1) / nx.number_of_nodes(graph)), (np.sum(arr_result) / nx.number_of_nodes(graph))
    return ave_indegree, ave_outdegree


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

