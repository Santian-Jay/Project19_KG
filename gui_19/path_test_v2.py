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
nodeNumber = 8
routeDic = {}
allRoutes = []
sign, residue = [], []
numberOfEdges = 0
subGraph = {}
all_sub = []

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


# def create_path(graph, list1):
#     temp = []
#     for i in range(len(list1) - 1):
#         graph.add_node(entityDic[list1[i]])
#         if i < len(list1) - 1:
#             if (list1[i], list1[i+1]) in big_dic:
#                 temp.append((list1[i], list1[i+1]))
#             else:
#                 temp.append((list1[i+1], list1[i]))
#     for item in list1:
#         addCount = 0
#         for item2 in big_dic:
#             if item in item2:
#                 if item2 not in temp:
#                     if addCount < 4:
#                         temp.append(item2)
#                         addCount += 1
#                     else:
#                         break
#     return temp
# file = open("dataset/YAGO3-10/train2id.txt", "r", encoding='UTF-8')

# entryNumber = (int)(file.readline())
G = nx.path_graph(0)
# for index in range(entryNumber):
#     content = file.readline()
#     head, tile, relation = content.strip().split()
#     nx.add_path(G, [int(head), int(tile)])
#     addEdge(int(head), int(tile))


def printRoute(stackList):
    global nodeNumber
    nodeNumber += 1
    G.node(str(nodeNumber), stackList[0])
    for node in stackList[1:]:
        nodeNumber += 1
        G.node(str(nodeNumber), node)
        G.edge(str(nodeNumber - 1), str(nodeNumber))


def findAllRoutes(start, end):
    global total
    stack.append(start)
    # print('current stack is: ', stack)
    if total >= 1:
        if start == end:
            print('找到路径： ', stack)
            stack.pop()
            total -= 1
        else:
            for nextPoint in edgeLinks[start]:
                if nextPoint not in stack: findAllRoutes(nextPoint, end)
            stack.pop()

# def findAR(start, end):
#      global graph, sign
#      stack1 = []
#      Sign()
#      stack1.append(start)
#      while len(stack1) != 0:
#          top = stack1[-1]
#          le = len(graph[top])
#          for i in graph[top]:
#              dst = graph[top].index(i)
#              if sign[top][dst] == 0 and i not in stack1:
#                  stack1.append(i)
#                  sign[top][dst] = 1
#                  break
#
#          if end in stack1:
#             print('stack1 is:  ', stack1)
#             stack1.pop()
#             continue
#          last = stack1[-1]
#          if last == top:
#              sign[top] = [0] * le
#              stack1.pop()


# def Sign():
#     global sign, residue
#     for i in  range(0,entryNumber):
#         le = len(residue[i])
#         sign[i] = [0] * le
G.add_edge(1, 2)
G.add_edge(1, 5)
G.add_edge(1, 6)
G.add_edge(1, 7)
G.add_edge(1, 17)
G.add_edge(1, 19)
G.add_edge(1, 3)
G.add_edge(2, 3)
G.add_edge(2, 8)
G.add_edge(2, 9)
G.add_edge(2, 10)
G.add_edge(3, 4)
G.add_edge(3, 11)
G.add_edge(3, 12)
G.add_edge(3, 13)
G.add_edge(4, 14)
G.add_edge(4, 15)
G.add_edge(4, 16)
G.add_edge(4, 17)
G.add_edge(4, 6)
G.add_edge(4, 18)
G.add_edge(18, 3)
G.add_edge(19, 2)
G.add_edge(13, 20)
G.add_edge(11, 21)
G.add_edge(12, 22)
G.add_edge(18, 23)
G.add_edge(16, 24)
G.add_edge(14, 25)
G.add_edge(15, 26)
G.add_edge(6, 26)
G.add_edge(5, 27)
G.add_edge(7, 28)
G.add_edge(19, 29)
G.add_edge(10, 30)
G.add_edge(8, 31)
G.add_edge(9, 32)
G.add_edge(2, 7)
G.add_edge(13, 28)
G.add_edge(16, 14)
G.add_edge(15, 25)
G.add_edge(26, 21)
G.add_edge(8, 29)
G.add_edge(12, 27)
G.add_edge(12, 29)



# G.add_edge(11, 5)
# G.add_edge(12, 5)
# G.add_edge(13, 5)
# G.add_edge(4, 1)
# print('计算图中节点1到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=4, target=1)])
# print('计算图中节点2到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=4, target=2)])
# print('0节点到4节点最短路径: ', nx.shortest_path(G, source=0, target=4))
# p1 = nx.shortest_path(G, source=5)
# print('0节点到所有节点最短路径: ', p1)
# print('计算图中节点0到节点4的所有最短路径: ', [p for p in nx.all_shortest_paths(G, source=0, target=4)])
# for q in nx.all_shortest_paths(G, source=0, target=4):
#     allRoutes.append(q)

# pos = nx.circular_layout(G)
# nx.draw(G, with_labels=True)

# findAllRoutes(0, 4)
# print(nx.has_path(G, 0, 4))
# print(nx.all_simple_edge_paths(G, 1, 4))
# for path in sorted(nx.all_simple_edge_paths(G, 1, 4)):
# for path in nx.all_simple_edge_paths(G, 1, 4):
    # print(path)

# print('all_simple_edge_paths')
# # for path in sorted(nx.all_simple_edge_paths(G, 0, 4)):
# for path in nx.all_simple_edge_paths(G, 1, 4):
#     print(path)
#
# # print('all_simple_paths')
# print('all_simple_paths')
# for path in nx.all_simple_paths(G, 1, 4):
#     print(path)

# a = {}
# print('shortest_simple_paths')
# for path in nx.shortest_simple_paths(G, 3, 5):
#     print(path)
#     if path[1] not in a:
#         if len(a) < 5:
#             a[path[1]] = []
#             a[path[1]].append(path)
#         else:
#             break
# length = 0
# for path in nx.shortest_simple_paths(G, 3, 5):
#     if len(a) < 5:
#         for i in a:
#             if path != a[i][0]:
#                 if i == path[1]:
#                     if length < 5:
#                         a[path[1]].append(path)
#                     for item in a:
#                         length = length + len(a[item])
#                     break
#
# print(len(a))
# print(a)

a = {}


# print('shortest_simple_paths')
# if nx.has_path(G, 3, 5):
#     for path in nx.shortest_simple_paths(G, 3, 5):
#         # print(path)
#         if path[1] not in a:
#             if len(a) < 5:
#                 a[path[1]] = []
#                 a[path[1]].append(path)
#             else:
#                 break
#     length = 0
#     for item in a:
#         length = length + len(a[item])
#     if length < 5 and len(a) < 5:
#         for path in nx.shortest_simple_paths(G, 3, 5):
#             if len(a) < 5:
#                 for i in a:
#                     if path != a[i][0]:
#                         if i == path[1]:
#                             if length < 5:
#                                 a[path[1]].append(path)
#                             for item in a:
#                                 length = length + len(a[item])
#                             break
# print(a)

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


# print(len(a[2]))
# print(allRoutes)
# print('total numberOfEdges', numberOfEdges)
# print('number_of_edges', nx.number_of_edges(G))
# print('number_of_nodes', nx.number_of_nodes(G))
# print('all routes list', allRoutes)
# print('edgelinks ', edgeLinks)
# print(in_degree)
# print(out_degree)

# path_list = []
# first_hop = list(G.neighbors(3))
# for f in first_hop:
#     path_list.append((3, f))
# print(path_list)
# G_F = nx.path_graph(0)
# for pl in path_list:
#     G_F.add_edge(pl[0], pl[1])

# pos = nx.circular_layout(G_F)
# nx.draw(G_F, with_labels=True)
# G_F = nx.path_graph()
# print(nx.number_of_nodes(G))
# print(nx.number_of_edges(G))
#
print("节点%d的邻居节点"% 3, list(G.neighbors(3)))
# print("节点%d的邻居节点"% 5, list(G.neighbors(5)))
# print("节点%d和节点%d的邻居节点" % (3,5), list(nx.common_neighbors(G, 3, 5)))

# path_list_2 = []
# second_hop = list(G.neighbors(5))
# for f in second_hop:
#     path_list_2.append((5, f))
# print(path_list)
# G_F_2 = nx.path_graph(0)
# for pl in path_list_2:
#     G_F_2.add_edge(pl[0], pl[1])
# pos = nx.circular_layout(G_F_2)
# nx.draw(G_F_2, with_labels=True)
# print("节点%d的邻居节点"% 5, list(G.neighbors(5)))
#
# temp = list(set(first_hop).union(set(second_hop)))
# print(sorted(temp))
# temp_2 = list(set(first_hop).intersection(set(second_hop)))
# print(sorted(temp_2))
# plt.show()


G_F_3 = nx.path_graph(0)
neighbors = {}
unique_key = []
def search_3_hop_nb(n1):
    if n1 not in neighbors:
        neighbors[n1] = []
    if n1 not in unique_key:
        unique_key.append(n1)
    list_1 = list(G.neighbors(n1))
    for l1 in list_1:  # 1, 27
        if (n1, l1) not in neighbors[n1]:
            neighbors[n1].append((n1, l1))
        if l1 not in neighbors:
            neighbors[l1] = []
        if l1 not in unique_key:
            unique_key.append(l1)
        for l2 in list(G.neighbors(l1)):  # 1: [2, 5, 6, 7, 17, 19, 3], 27: [5, 12]
            if (l1, l2) not in neighbors[l1]:
                neighbors[l1].append((l1, l2))
            if l2 not in neighbors:
                neighbors[l2] = []
            if l2 not in unique_key:
                unique_key.append(l2)
            for l3 in list(G.neighbors(l2)):  # 1: [2, 5, 6, 7, 17, 19, 3], 27: [5, 12]
                if (l2, l3) not in neighbors[l2]:
                    neighbors[l2].append((l2, l3))
                # if l3 not in unique_key:
                #     unique_key.append(l3)

search_3_hop_nb(5)
search_3_hop_nb(3)
search_3_hop_nb(1)
# print(neighbors)
print('unique_key: ', sorted(unique_key))
# print("节点%d的邻居节点"% 1, list(G.neighbors(1)))
# print("节点%d的邻居节点"% 27, list(G.neighbors(27)))
print('neighbors', neighbors)

path_list_final = {}
for item in unique_key:
    for double in neighbors[item]:
        if double not in path_list_final and tuple(reversed(double)) not in path_list_final:
            path_list_final[double] = 0
print(path_list_final)
print(len(path_list_final))


for pl in path_list_final:
    G_F_3.add_edge(pl[0], pl[1])
pos = nx.circular_layout(G_F_3)
nx.draw(G_F_3, with_labels=True)
print('number_of_edges', nx.number_of_edges(G_F_3))
print('number_of_nodes', nx.number_of_nodes(G_F_3))
# plt.show()

a = {}
# a = {(1,2):0, (2, 1):0}
# print((1, 2) in a)
b = [(2,1, 1), (2,1, 2)]
for i in b:
    a[i] = 0
# print(tuple(reversed(b)))
# if b not in a and reversed(b) not in a:
#     a[b] = 0
# if b not in a and reversed(b) not in a:
#     a[b] = 0
print(a)