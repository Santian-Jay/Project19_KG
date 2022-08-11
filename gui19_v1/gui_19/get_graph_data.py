import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def clear_dataset(data, new):
    for i in data:
        first = i.strip('\n')  # delete '\n'
        second = first.split()  # delete 'space'
        if len(i) != 1:
            new.append(second)  # add data into list


def get_degree(graph, in_d, out_d):
    As_1 = nx.adjacency_matrix(graph, weight=None)  # Ignore weights when converting to matrix 'weight=None'
    A_1 = As_1.todense()
    result = np.sum(A_1, axis=1)
    result_1 = np.sum(A_1, axis=0)

    arr_result = np.array(result)
    arr_result_1 = np.array(result_1)


    print("out degree： \n", result)  # out degree list
    print("in degree： ", result_1)  # in degree list
    print("average in degree： ", np.sum(arr_result_1) / nx.number_of_nodes(graph))  # in degree list
    print("average out degree： ", np.sum(arr_result) / nx.number_of_nodes(graph))  # in degree list

    # in_d = np.sum(arr_result_1) / nx.number_of_nodes(graph)
    # out_d = np.sum(arr_result) / nx.number_of_nodes(graph)

    # print("node {} out degree： {}\n".format(node, arr_result[node][0]))  # out degree of specified node, if index include '0', then don't need -1
    # print("node {} in degree： {}".format(node, arr_result_1[0][node]))  # in degree of specified node


G = nx.MultiDiGraph()  # multiple directed graph
n_relation = 0
n_entity = 0
n_edge = 0

class GraphInformation:
    def __init__(self):
        self.n_enti, self.n_rela,self.n_edg  = self.draw_graph()
        self.in_d = self.get_in_degree(G)
        self.out_d = self.get_out_degree(G)

        # self.n_rela = n_relation
        # self.n_edg = n_edge
        print(self.in_d, self.out_d, self.n_enti, self.n_rela, self.n_edg)

    def get_data(self):
        return self.in_d, self.out_d

    def get_entity(self, graph):
        return nx.number_of_nodes(G)

    def get_edge(self, graph):
        return nx.number_of_edges(G)

    def get_out_degree(self, graph):
        As_1 = nx.adjacency_matrix(graph, weight=None)  # Ignore weights when converting to matrix 'weight=None'
        A_1 = As_1.todense()
        result = np.sum(A_1, axis=1)
        result_1 = np.sum(A_1, axis=0)

        arr_result = np.array(result)
        arr_result_1 = np.array(result_1)
        return np.sum(arr_result) / nx.number_of_nodes(graph)


    def get_in_degree(self, graph):
        As_1 = nx.adjacency_matrix(graph, weight=None)  # Ignore weights when converting to matrix 'weight=None'
        A_1 = As_1.todense()
        result = np.sum(A_1, axis=1)
        result_1 = np.sum(A_1, axis=0)

        arr_result = np.array(result)
        arr_result_1 = np.array(result_1)
        return np.sum(arr_result_1) / nx.number_of_nodes(graph)


    def draw_graph(self):
        # G = nx.MultiDiGraph()  # multiple directed graph
        G.clear()
        f_train = open('dataset/train2id.txt', 'r')
        all_train = f_train.readlines()
        new_train, feature_1, feature_2, weight, relation, entity, tail = [], [], [], [], [], [], []

        clear_dataset(all_train, new_train)

        # print(new_train)
        for train in new_train:
            if len(train) != 1:
                feature_1.append(int(train[0]))
                feature_2.append(int(train[1]))
                weight.append(int(train[2]))

        for i in weight:
            if i not in relation:
                relation.append(i)

        for n in feature_1:
            if n not in entity:
                entity.append(n)

        for t in feature_2:
            if t not in entity:
                entity.append(t)
        entity = sorted(entity)
        relation = sorted(relation)

        G.clear()
        # n_relation = len(relation)
        # n_entity = nx.number_of_nodes(G)
        # n_edge = nx.number_of_edges(G)

        # n_relation = len(relation)
        # n_entity = nx.number_of_nodes(G)
        # n_edge = nx.number_of_edges(G)
        # print(n_entity, n_edge, n_relation)
        for edge in new_train:
            if len(edge) != 1:
                G.add_weighted_edges_from([(edge[0], edge[1], int(edge[2]))], weight=int(edge[2]))
                # G.add_edge(edge[0], edge[1])

        n_entity = nx.number_of_nodes(G)
        n_edge = nx.number_of_edges(G)
        n_relation = len(relation)

        return n_entity, n_relation, n_edge

        # print(n_entity, n_edge, n_relation)

        # pos = nx.spring_layout(G, k=10)

        # degree = nx.degree_histogram(G)
        # x = range(len(degree))
        # y = [z/float(sum(degree)) for z in degree]

        # nx.draw(G, pos=pos, with_labels=True)

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
        # plt.show()


gi = GraphInformation()

if __name__ == '__main__':
    gi.draw_graph()
