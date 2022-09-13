import itertools

import networkx as nx
import sys

sys.setrecursionlimit(400000)
import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph

total = 10
edgeLinks = dict()
in_degree = dict()
out_degree = dict()
stack = []
new = []
nodeNumber = 8
routeDic = {}
allRoutes = []
sign, residue = [], []
numberOfEdges = 0
count = 0
searchList = [0, 1, 4, 3, 5]
all_shortest_path = {}
tempList = []
used_routes = []
all_sub = []
temp1 = []
big_dic = {}
relatesDic = {}
entityDic = {}
neighborNode = {}

entity = r'./dataset/entity2id.txt'
relate = r'./dataset/relation2id.txt'
# entity = r'./dataset/entity2id.txt'
# relate = r'./dataset/relation2id.txt'

def get_relate(file):
    with open(file, 'r', encoding='UTF-8') as f:
        next(f)
        for line in f:
            name, index = line.strip().split()
            relatesDic[int(index)] = name


def get_entity(file):
    with open(file, 'r', encoding='UTF-8') as f:
        next(f)
        for line in f:
            name, index = line.strip().split()
            entityDic[int(index)] = name


get_relate(relate)
get_entity(entity)

def create_path(graph, list1):
    temp = []
    for i in range(len(list1) - 1):
        graph.add_node(entityDic[list1[i]])
        if i < len(list1) - 1:
            if (list1[i], list1[i+1]) in big_dic:
                temp.append((list1[i], list1[i+1]))
            else:
                temp.append((list1[i+1], list1[i]))
    for item in list1:
        addCount = 0
        for item2 in big_dic:
            if item in item2:
                if item2 not in temp:
                    if addCount < 4:
                        temp.append(item2)
                        addCount += 1
                    else:
                        break
    return temp



def addEdge(a, b):
    global numberOfEdges
    numberOfEdges += 1
    # global edgeLinks
    if a not in edgeLinks: edgeLinks[a] = set()
    if b not in edgeLinks: edgeLinks[b] = set()
    if a not in in_degree: in_degree[a] = 0
    if b not in in_degree: in_degree[b] = 0
    if a not in out_degree: out_degree[a] = 0
    if b not in out_degree: out_degree[b] = 0
    edgeLinks[a].add(b)
    edgeLinks[b].add(a)
    in_degree[b] += 1
    out_degree[a] += 1
file = open("dataset/train2id.txt", "r", encoding='UTF-8')

entryNumber = (int)(file.readline())
G = nx.path_graph(1)
for index in range(entryNumber):
    content = file.readline()
    head, tile, relation = content.strip().split()
    big_dic[(int(head), int(tile))] = int(relation)
    nx.add_path(G, [int(head), int(tile)])
    addEdge(int(head), int(tile))


a = {}

list_1 = list(G.neighbors(4))
print(list_1)
print('shortest_simple_paths')
if nx.has_path(G, 4, 5):
    # for path in nx.shortest_simple_paths(G, 4, 5):
    for path in nx.all_simple_paths(G, 4, 5):
        print(path)
        if path[1] not in a:
            if len(a) < 5:
                a[path[1]] = []
                a[path[1]].append(path)
            else:
                break
    length = 0
    for item in a:
        length = length + len(a[item])
    if length < 5 and len(a) < 5:
        # for path in nx.shortest_simple_paths(G, 4, 5):
        for path in nx.all_simple_paths(G, 4, 5):
            if len(a) < 5:
                for i in a:
                    if path != a[i][0]:
                        if i == path[1]:
                            if length < 5:
                                a[path[1]].append(path)
                            for item in a:
                                length = length + len(a[item])
                            break
print(a)
# graphList = []
#
# for p in a:
#     sub_graph = nx.MultiDiGraph()
#     graphList.append(sub_graph)
#     if len(a[p]) > 1:
#         for item in a[p]:
#             all_sub.append(create_path(sub_graph, item))
#     else:
#         all_sub.append(create_path(sub_graph, a[p][0]))
#
#
#
# # print('neighbor: ', neighborNode)
# # print(len(a))
# print(a)
# # print('all path')
# # print(all_sub)
# print('big_dic: ', big_dic)
# print('big_dic length: ', len(big_dic))
#
#
#
#
#
# def draw_sub(sub, index):
#     old_attrs = nx.get_edge_attributes(sub, 'weight')
#     attrs = {}
#     for k, v in old_attrs.items():
#          attrs[(k[0], k[1])] = v
#     pos = nx.circular_layout(sub)
#     # node
#     plt.figure(dpi=160, figsize=(12, 8))
#     nx.draw_networkx_nodes(sub, pos, node_size=400, node_color='#6495ED')
#     label_options = {"ec": "k", "fc": "white", "alpha": 0.5}
#     nx.draw_networkx_labels(sub, pos, font_size=10, bbox=label_options)
#     # edge
#     nx.draw_networkx_edges(sub, pos)
#
#     nx.draw_networkx_edge_labels(sub, pos, edge_labels=attrs)
#     plt.axis('off')
#     save_path = 'subgraph_images/picture-{}.png'.format(index + 1)
#     plt.savefig(save_path)
#
#
#
# for g in range(len(all_sub)):
#     for i in all_sub[g]:
#         reverse = tuple(reversed(i))
#         if i not in big_dic:
#             r = big_dic[reverse]
#             graphList[g].add_edge(entityDic[reverse[0]], entityDic[reverse[1]], weight=relatesDic[r])
#         else:
#             r = big_dic[i]
#             graphList[g].add_edge(entityDic[i[0]], entityDic[i[1]], weight=relatesDic[r])
#     draw_sub(graphList[g], g)
